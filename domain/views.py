from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Count
from django.db.models.query import QuerySet
from django.forms.formsets import formset_factory
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from tagging.models import Tag, TaggedItem
from common.constants import STATUS_PUBLISHED, STATUS_DRAFT, STATUS_PENDING
from common.decorators import statistic
from common.functions import people_render_reference, topic_render_reference, statement_render_reference, process_status, \
    get_success_message
from domain.forms import PeopleEditForm, TopicEditForm, StatementEditForm, ReferenceForm
from domain.models import People, Topic, Statement, Meter, PeopleCategory


# =============================
# Global
# =============================

@login_required
def domain_delete(request, inst_name, id):

    inst = get_object_or_404(eval(inst_name.title()), pk=id)

    if (hasattr(inst, 'created_by') and request.user.id == inst.created_by.id) or request.user.is_staff:
        inst.delete()
    else:
        raise Http404('No item matches the given query.')

    messages.success(request, _('Your %s has been deleted.') % inst_name)
    return redirect('home')



def statement_query_base(is_anonymous=True, is_staff=False, user=None):

    statement_list = Statement.objects.all()

    if is_anonymous:
        statement_list = statement_list.exclude(status__in=[STATUS_DRAFT, STATUS_PENDING])

        statement_list = statement_list.extra(select={'uptodate': '%s(COALESCE(created, "1000-01-01"), COALESCE(changed, "1000-01-01"))' % settings.GREATEST_FUNCTION})


    else:

        if is_staff:
            statement_list = statement_list.filter(Q(status__in=[STATUS_PUBLISHED, STATUS_PENDING])|Q(created_by=user))

        else:
            statement_list = statement_list.filter(Q(status__in=[STATUS_PUBLISHED])|Q(created_by=user, status__in=[STATUS_DRAFT, STATUS_PENDING]))

        statement_list = statement_list.extra(select={'uptodate': '%s(COALESCE(created_raw, "1000-01-01"), COALESCE(created, "1000-01-01"), COALESCE(changed, "1000-01-01"))' % settings.GREATEST_FUNCTION})

    return statement_list


# =============================
# Home
# =============================

def home(request):

    statement_list = statement_query_base(is_anonymous=True)

    hilight_statement = statement_list.order_by('-hilight', '-promote', '-uptodate')[0:1]

    meter_list = Meter.objects.all().order_by('order')

    meter_statement_count = [(meter, meter.statement_set.count()) for meter in meter_list]

    statement_list = statement_list.exclude(id__in=[s.id for s in hilight_statement]).order_by('-promote', '-uptodate')

    hilight_statement = list(hilight_statement)
    hilight_statement.append(None)
    hilight_statement = hilight_statement[0]


    meter_statement_list = [({'title': 'Latest', 'permalink': 'latest'}, statement_list[0:4])]
    for meter in meter_list:

        meter_statement = statement_list.filter(meter=meter)[0:3]
        meter_statement_list.append((meter, meter_statement))

    tags_list = Tag.objects.usage_for_model(Statement, counts=True)
    tags_list.sort(key=Count, reverse=True)
    tags_list = tags_list[0:15]

    return render(request, 'domain/home.html', {
        'hilight_statement': hilight_statement,
        'meter_statement_count': meter_statement_count,
        'meter_statement_list': meter_statement_list,
        'tags_list': tags_list,
        'contact_footer': render_to_string('contact_footer.txt')
    })


# =============================
# People
# =============================

@login_required
def people_create(request, people=None):

    people = people or People()

    if request.method == 'POST':
        form = PeopleEditForm(people, People, request.POST)

        is_new = form.is_new()

        if form.is_valid():
            people.permalink = form.cleaned_data['permalink']
            people.first_name = form.cleaned_data['first_name']
            people.last_name = form.cleaned_data['last_name']
            people.occupation = form.cleaned_data['occupation']
            people.description = form.cleaned_data['description']
            people.homepage_url = form.cleaned_data['homepage_url']
            people.image = form.cleaned_data['image']

            # Use save_form_data like model form
            people.image._field.save_form_data(people, form.cleaned_data['image'])
            people.status = int(STATUS_PUBLISHED if form.cleaned_data['status'] == '' else form.cleaned_data['status'])
            people.created_by = request.user
            people.save()

            people.categories.clear()
            for category in form.cleaned_data['categories']:
                people.categories.add(category)

            message_success = get_success_message(people, is_new)

            if request.GET.get('_popup'):
                message_success = '<script type="text/javascript"> opener.dismissAddAnotherPopup(window, \'%s\', \'%s\'); </script>' % (people.id, people_render_reference(people))

            messages.success(request, message_success)

            return redirect('people_edit', people.id)
    else:
        initial = {
            'permalink': people.permalink,
            'first_name': people.first_name,
            'last_name': people.last_name,
            'occupation': people.occupation,
            'description': people.description,
            'homepage_url': people.homepage_url,
            'image': people.image,
            'status': people.status,
        }

        if people.id:
            initial['categories'] = people.categories.all()


        form = PeopleEditForm(people, People, initial=initial)


    return render(request, 'domain/people_form.html', {
        'form': form
    })


@login_required
def people_edit(request, people_id=None):

    people = get_object_or_404(People, pk=people_id)
    return people_create(request, people)


def people_detail(request, people_permalink):

    people = get_object_or_404(People, permalink=people_permalink)

    meter_list = Meter.objects.all().order_by('order')
    meter_statement_count = [(meter, meter.statement_set.filter(quoted_by=people).count()) for meter in meter_list]

    statement_list = statement_query_base(request.user.is_anonymous(), request.user.is_staff, request.user)
    statement_list = statement_list.filter(Q(quoted_by=people)|Q(relate_peoples=people)).order_by('-uptodate')


    return render(request, 'domain/people_detail.html', {
        'people': people,
        'meter_statement_count': meter_statement_count,
        'statement_list': statement_list
    })


def people_list(request):

    # Force MYSQL Distinct
    query = People.objects.all().order_by('-quoted_by__created').query
    query_str = query.__str__()
    query_str = query_str.replace('SELECT', 'SELECT DISTINCT')

    people_list = People.objects.raw(query_str)


    category_list = PeopleCategory.objects.all()

    return render(request, 'domain/people_list.html', {
        'people_list': people_list,
        'category_list': category_list
    })


# =============================
# Tags
# =============================

def tags_detail(request, tags_id):

    return render(request, 'domain/tags_detail.html', {
        'tags': None,
        'statement_list': []
    })


# =============================
# Meter
# =============================

def meter_detail(request, meter_permalink):

    return render(request, 'domain/meter_detail.html', {
        'meter': None,
        'statement_list': []
    })


def meter_list(request):

    return meter_detail(request, '')


# =============================
# Topic
# =============================

@login_required
def topic_create(request, topic=None):

    topic = topic or Topic()

    if request.method == 'POST':

        if request.POST.get('as_revision') is None or not int(request.POST.get('as_revision')):
            request.POST['as_revision'] = None

        form = TopicEditForm(topic, Topic, request.POST)

        is_new = form.is_new()

        if form.is_valid():
            topic.title = form.cleaned_data['title']
            topic.description = form.cleaned_data['description']
            topic.created_by = request.user

            as_revision = form.cleaned_data['as_revision']
            without_revision = not as_revision

            topic.save(without_revision=without_revision)

            message_success = get_success_message(topic, is_new)

            if request.GET.get('_popup'):
                message_success = '<script type="text/javascript"> opener.dismissAddAnotherPopup(window, \'%s\', \'%s\'); </script>' % (topic.id, topic_render_reference(topic))


            if request.GET.get('_inline') or request.POST.get('_inline'):
                form.inst = topic
            else:
                messages.success(request, message_success)
                return redirect('topic_edit', topic.id)
    else:
        initial = {
            'title': topic.title,
            'description': topic.description,
            'as_revision': True,
        }

        form = TopicEditForm(topic, Topic, initial=initial)


    if request.GET.get('_inline') or request.POST.get('_inline'):
        return render(request, 'domain/topic_inline_form.html', {
            'form': form
        })


    return render(request, 'domain/topic_form.html', {
        'form': form
    })


@login_required
def topic_edit(request, topic_id=None):

    topic = get_object_or_404(Topic, pk=topic_id)
    return topic_create(request, topic)


@login_required
def topic_edit_from_statement(request, topic_id, statement_id):

    statement = get_object_or_404(Statement, pk=statement_id, topic_id=topic_id)
    response = topic_edit(request, topic_id)

    if response.status_code == 302 and request.POST.get('as_revision'):

        statement.save()

    return response

def topic_detail(request, topic_id):
    return HttpResponse('Fixed me !!')


# =============================
# Statement
# =============================

@login_required
def statement_create(request, statement=None):

    statement = statement or Statement()


    ReferenceFormSet = formset_factory(ReferenceForm, extra=2, can_delete=True)


    if request.method == 'POST':

        form = StatementEditForm(statement, Statement, request.POST)
        reference_formset = ReferenceFormSet(request.POST, prefix='references')

        is_new = form.is_new()

        if form.is_valid() and reference_formset.is_valid():
            statement.permalink = form.cleaned_data['permalink']
            statement.quote = form.cleaned_data['quote']
            statement.created_by = request.user
            statement.quoted_by_id = form.cleaned_data['quoted_by'].id
            statement.source = form.cleaned_data['source']
            statement.topic_id = form.cleaned_data['topic'].id if form.cleaned_data['topic'] else None
            statement.tags = form.cleaned_data['tags']
            statement.meter_id = form.cleaned_data['meter'].id

            status = int(form.cleaned_data['status'])
            statement.status = process_status(request.user, status) if not statement.published else status

            statement.hilight = form.cleaned_data['hilight']
            statement.promote = form.cleaned_data['promote']

            if not statement.published and statement.status == STATUS_PUBLISHED:
                statement.published = timezone.now()
                statement.published_by = request.user

            # Save references
            references = []
            for reference_form in reference_formset:

                if reference_form.cleaned_data and not reference_form.cleaned_data.get('DELETE'):

                    references.append({
                        'url': reference_form.cleaned_data['url'],
                        'title': reference_form.cleaned_data['title']
                    })

            statement.references = references

            statement.save()

            statement.relate_statements.clear()
            for relate_statement in form.cleaned_data['relate_statements']:
                statement.relate_statements.add(relate_statement)

            statement.relate_peoples.clear()
            for relate_people in form.cleaned_data['relate_peoples']:
                statement.relate_peoples.add(relate_people)

            message_success = get_success_message(statement, is_new)

            if request.GET.get('_popup'):
                message_success = '<script type="text/javascript"> opener.dismissAddAnotherPopup(window, \'%s\', \'%s\'); </script>' % (statement.id, statement_render_reference(statement))


            messages.success(request, message_success)

            return redirect('statement_edit', statement.id)
    else:
        initial = {
            'permalink': statement.permalink,
            'quote': statement.quote,
            'status': statement.status,
            'quoted_by': statement.quoted_by_id,
            'source': statement.source,
            'topic': statement.topic_id,
            'tags': statement.tags,
            'meter': statement.meter_id or Meter.objects.get(permalink='unverifiable').id,
            'hilight': statement.hilight,
            'promote': statement.promote
        }

        if statement.id:
            initial['relate_statements'] = statement.relate_statements.all()
            initial['relate_peoples'] = statement.relate_peoples.all()
        else:
            initial['status'] = process_status(request.user, initial['status'], True)

        form = StatementEditForm(statement, Statement, initial=initial)

        reference_formset = ReferenceFormSet(initial=statement.references, prefix='references')


    return render(request, 'domain/statement_form.html', {
        'form': form,
        'reference_formset': reference_formset,
    })


@login_required
def statement_edit(request, statement_id=None):

    statement = get_object_or_404(Statement, pk=statement_id)
    return statement_create(request, statement)


@statistic
def statement_detail(request, statement_permalink):

    statement = get_object_or_404(Statement, permalink=statement_permalink)

    return render(request, 'domain/statement_detail.html', {
        'statement': statement,
        'meter_list': Meter.objects.all().order_by('order')
    })




def statement_list(request):

    statement_list = statement_query_base(request.user.is_anonymous(), request.user.is_staff, request.user)
    statement_list = statement_list.order_by('-uptodate')

    paginator = Paginator(statement_list, 10)

    page = request.GET.get('page')
    try:
        statement_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        statement_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        statement_list = paginator.page(paginator.num_pages)

    from tagging.models import Tag

    return render(request, 'domain/statement_list.html', {
        'statement_list': statement_list,
        'meter_list': Meter.objects.all().order_by('order'),
        'tags_list': Tag.objects.all()
    })
