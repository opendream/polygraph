from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Count, Max
from django.db.models.query import QuerySet
from django.forms.formsets import formset_factory
from django.http import Http404, HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_tables2 import RequestConfig
from tagging.models import Tag, TaggedItem
from common.constants import STATUS_PUBLISHED, STATUS_DRAFT, STATUS_PENDING
from common.decorators import statistic
from common.functions import people_render_reference, topic_render_reference, statement_render_reference, process_status, \
    get_success_message, image_render
from domain.forms import PeopleEditForm, TopicEditForm, StatementEditForm, ReferenceForm
from domain.models import People, Topic, Statement, Meter, PeopleCategory, TopicRevision


# =============================
# Global
# =============================
from domain.tables import StatementTable, MyStatementTable, PeopleTable, MyPeopleTable


@login_required
def domain_delete(request, inst_name, id):

    inst = get_object_or_404(eval(inst_name.title()), id=id)

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


def pagination_build_query(request, item_list, ipp=10):

    paginator = Paginator(item_list, ipp)

    page = request.GET.get('page')
    try:
        item_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        item_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        item_list = paginator.page(paginator.num_pages)

    return item_list


# =============================
# Home
# =============================

def home(request):

    statement_list = statement_query_base(is_anonymous=True)

    hilight_statement = statement_list.order_by('-hilight', '-promote', '-uptodate')[0:1]

    meter_list = Meter.objects.all().order_by('order')

    meter_statement_count = [(meter, meter.statement_set.filter(status=STATUS_PUBLISHED).count()) for meter in meter_list]

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
            people.summary = form.cleaned_data['summary']
            people.description = form.cleaned_data['description']
            people.homepage_url = form.cleaned_data['homepage_url']
            people.image = form.cleaned_data['image']

            # Use save_form_data like model form
            if people.image:
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
            'summary': people.summary,
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

    people = get_object_or_404(People, id=people_id)
    return people_create(request, people)


@statistic
def people_detail(request, people_permalink):

    people = get_object_or_404(People, permalink=people_permalink)

    meter_list = Meter.objects.all().order_by('order')
    meter_statement_count = [(meter, meter.statement_set.filter(status=STATUS_PUBLISHED, quoted_by=people).count()) for meter in meter_list]

    statement_list = statement_query_base(request.user.is_anonymous(), request.user.is_staff, request.user)
    statement_list = statement_list.filter(Q(quoted_by=people)|Q(relate_peoples=people)).order_by('-uptodate')


    statement_list = pagination_build_query(request, statement_list, 5)


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


    people_list = People.objects.all().order_by('-quoted_by__created')

    category = None
    if request.GET.get('category'):
        category = get_object_or_404(PeopleCategory, permalink=request.GET.get('category'))
        people_list = people_list.filter(categories=category)


    query = people_list.query
    query.group_by = ['id']

    # SQL injection hack by developer for order MAX uptodate
    query.order_by.append('-is_deleted`, MAX(%s(COALESCE(`domain_statement.created, "1000-01-01"), COALESCE(domain_statement.changed, "1000-01-01")))' % settings.GREATEST_FUNCTION)

    query.order_by.reverse()

    people_list = QuerySet(query=query, model=People)


    people_list = pagination_build_query(request, people_list, 10)



    category_list = PeopleCategory.objects.all()

    return render(request, 'domain/people_list.html', {
        'people_list': people_list,
        'category_list': category_list,
        'request_category': category

    })



# =============================
# Meter
# =============================

@statistic
def meter_detail(request, meter_permalink=None):

    meter_list = Meter.objects.all().order_by('order')

    if not meter_permalink:
        meter = meter_list[0]
    else:
        meter = get_object_or_404(Meter, permalink=meter_permalink)

    statement_list = statement_query_base(request.user.is_anonymous(), request.user.is_staff, request.user)
    statement_list = statement_list.filter(meter=meter).order_by('-uptodate')

    statement_list = pagination_build_query(request, statement_list, 10)


    return render(request, 'domain/meter_detail.html', {
        'request_meter': meter,
        'meter_list': meter_list,
        'statement_list': statement_list
    })


# =============================
# Topic
# =============================

@login_required
def topic_create(request, topic=None):

    topic = topic or Topic()

    if request.method == 'POST':

        if request.POST.get('as_revision') is None or not int(request.POST.get('as_revision')):
            request.POST = request.POST.copy()
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

    topic = get_object_or_404(Topic, id=topic_id)
    return topic_create(request, topic)


@login_required
def topic_edit_from_statement(request, topic_id, statement_id):

    statement = get_object_or_404(Statement, id=statement_id, topic_id=topic_id)
    response = topic_edit(request, topic_id)

    if response.status_code == 302 and request.POST.get('as_revision'):

        statement.save()

    return response


@statistic
def topic_detail(request, topic_id, topicrevision_id=False):

    origin = get_object_or_404(Topic, id=topic_id)

    meter_list = Meter.objects.all().order_by('order')
    meter_statement_count = [(meter, meter.statement_set.filter(status=STATUS_PUBLISHED).count()) for meter in meter_list]

    statement_list = statement_query_base(request.user.is_anonymous(), request.user.is_staff, request.user)
    statement_list = statement_list.filter(topic=origin).order_by('-uptodate')


    statement_list = pagination_build_query(request, statement_list, 5)

    if topicrevision_id:
        topic = get_object_or_404(TopicRevision, origin=origin, id=topicrevision_id)
    else:
        topic = origin

    return render(request, 'domain/topic_detail.html', {
        'origin': origin,
        'topic': topic,
        'meter_statement_count': meter_statement_count,
        'statement_list': statement_list,

    })


def topic_list(request):
    return HttpResponse('Fixed me !!')


# =============================
# Topic Revision
# =============================

def topicrevision_detail(request, topic_id, topicrevision_id):
    return topic_detail(request, topic_id, topicrevision_id)


@login_required
def topicrevision_edit(request, topic_id, topicrevision_id):

    topic = get_object_or_404(TopicRevision, origin__id=topic_id, id=topicrevision_id)
    return topic_create(request, topic)



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
            statement.short_detail = form.cleaned_data['short_detail']
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
            'short_detail': statement.short_detail,
            'status': statement.status,
            'quoted_by': statement.quoted_by and statement.quoted_by.id,
            'source': statement.source,
            'topic': statement.topic and statement.topic.id,
            'tags': statement.tags,
            'meter': statement.meter and (statement.meter.id or Meter.objects.get(permalink='unverifiable').id),
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

    statement = get_object_or_404(Statement, id=statement_id)
    return statement_create(request, statement)


@statistic
def statement_detail(request, statement_permalink):

    statement = get_object_or_404(Statement, permalink=statement_permalink)
    try:
        topicrevision = TopicRevision.objects.filter(origin=statement.topic).latest('id')
    except TopicRevision.DoesNotExist:
        topicrevision = None


    return render(request, 'domain/statement_detail.html', {
        'statement': statement,
        'topic': topicrevision,
        'meter_list': Meter.objects.all().order_by('order'),
        'meter_image': statement.meter.image_small_text.thumbnail_200x200()
    })

def statement_topicrevision_detail(request, statement_permalink, topicrevision_id):

    statement = get_object_or_404(Statement, permalink=statement_permalink)
    topicrevision = get_object_or_404(TopicRevision, id=topicrevision_id)


    return render(request, 'domain/statement_detail.html', {
        'statement': statement,
        'topic': topicrevision,
        'meter_list': Meter.objects.all().order_by('order')
    })


def statement_list(request, tags_id=None):

    statement_list = statement_query_base(request.user.is_anonymous(), request.user.is_staff, request.user)

    tags = None
    if tags_id:
        tags = get_object_or_404(Tag, id=tags_id)
        statement_list = statement_list.filter(tags__contains=tags.name)

    statement_list = statement_list.order_by('-uptodate')

    statement_list = pagination_build_query(request, statement_list, 10)


    return render(request, 'domain/statement_list.html', {
        'statement_list': statement_list,
        'meter_list': Meter.objects.all().order_by('order'),
        'tags_list': Tag.objects.all(),
        'request_tags': tags
    })


def statement_tags_detail(request, tags_id):

    return statement_list(request, tags_id)


# =============================
# Manage
# =============================
@login_required
def manage(request):
    raise Http404('No Implement Yet.')


@login_required
def manage_my_statement(request):

    item_list = Statement.objects.all().order_by('-created', '-id').filter(created_by=request.user)
    table = MyStatementTable(item_list)
    RequestConfig(request).configure(table)

    return render(request, 'manage.html', {'table': table, 'page_title': _('Manage My Statements')})


@staff_member_required
def manage_pending_statement(request):

    item_list = Statement.objects.all().order_by('-created', '-id').filter(status=STATUS_PENDING).exclude(status=STATUS_DRAFT)
    table = StatementTable(item_list)
    RequestConfig(request).configure(table)

    return render(request, 'manage.html', {'table': table, 'page_title': _('Manage Pending Statements')})


@staff_member_required
def manage_hilight_statement(request):

    item_list = Statement.objects.all().order_by('-created', '-id').filter(hilight=True).exclude(status=STATUS_DRAFT)
    table = StatementTable(item_list)
    RequestConfig(request).configure(table)

    return render(request, 'manage.html', {'table': table, 'page_title': _('Manage Highlight Statements')})


@staff_member_required
def manage_promote_statement(request):

    item_list = Statement.objects.all().order_by('-created', '-id').filter(promote=True).exclude(status=STATUS_DRAFT)
    table = StatementTable(item_list)
    RequestConfig(request).configure(table)

    return render(request, 'manage.html', {'table': table, 'page_title': _('Manage Promote Statements')})


@staff_member_required
def manage_statement(request):

    item_list = Statement.objects.all().order_by('-created', '-id').exclude(status=STATUS_DRAFT)
    table = StatementTable(item_list)
    RequestConfig(request).configure(table)

    return render(request, 'manage.html', {'table': table, 'page_title': _('Manage All Statements')})


@login_required
def manage_my_people(request):

    item_list = People.objects.all().order_by('-created', '-id').filter(created_by=request.user)
    table = MyPeopleTable(item_list)
    RequestConfig(request).configure(table)

    return render(request, 'manage.html', {'table': table, 'page_title': _('Manage My People')})


@staff_member_required
def manage_people(request):

    item_list = People.objects.all().order_by('-created', '-id').exclude(status=STATUS_DRAFT)
    table = PeopleTable(item_list)
    RequestConfig(request).configure(table)

    return render(request, 'manage.html', {'table': table, 'page_title': _('Manage All People')})


