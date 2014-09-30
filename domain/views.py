import os
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.db.models import Q, Count, Max
from django.db.models.query import QuerySet
from django.forms.formsets import formset_factory
from django.http import Http404, HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.vary import vary_on_cookie

from django_tables2 import RequestConfig
from tagging.models import Tag, TaggedItem
from common.constants import STATUS_PUBLISHED, STATUS_DRAFT, STATUS_PENDING
from common.decorators import statistic, scache
from django.views.decorators.cache import never_cache, cache_page
from common.functions import people_render_reference, topic_render_reference, statement_render_reference, process_status, \
    get_success_message, image_render, set_default_value
from common.models import Variable
from domain.forms import PeopleEditForm, TopicEditForm, StatementEditForm, ReferenceForm, InformationForm
from domain.models import People, Topic, Statement, Meter, PeopleCategory, TopicRevision
from common.tasks import generate_statement_card, warm_cache

# =============================
# Global
# =============================
from domain.tables import StatementTable, MyStatementTable, PeopleTable, MyPeopleTable, SortableStatementTable


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

        statement_list = statement_list.extra(select={'uptodate': '%s(COALESCE(domain_statement.created, "1000-01-01"), COALESCE(domain_statement.changed, "1000-01-01"))' % settings.GREATEST_FUNCTION})


    else:

        if is_staff:
            statement_list = statement_list.filter(Q(status__in=[STATUS_PUBLISHED, STATUS_PENDING])|Q(created_by=user))

        else:
            statement_list = statement_list.filter(Q(status__in=[STATUS_PUBLISHED])|Q(created_by=user, status__in=[STATUS_DRAFT, STATUS_PENDING]))

        statement_list = statement_list.extra(select={'uptodate': '%s(COALESCE(domain_statement.created_raw, "1000-01-01"), COALESCE(domain_statement.created, "1000-01-01"), COALESCE(domain_statement.changed, "1000-01-01"))' % settings.GREATEST_FUNCTION})

    #statement_list = statement_list.select_related('quoted_by', 'created_by', 'meter')
    statement_list = statement_list.prefetch_related('quoted_by', 'created_by', 'meter')

    return statement_list


def people_query_base(category=None, is_anonymous=True, is_staff=False, user=None):


    people_list = People.objects.all().order_by('-quoted_by__hilight', '-quoted_by__promote', '-quoted_by__changed', '-quoted_by__created')

    if category:
        category = get_object_or_404(PeopleCategory, permalink=category)
        people_list = people_list.filter(categories=category)

    if is_anonymous:
        people_list = people_list.exclude(status__in=[STATUS_DRAFT, STATUS_PENDING])

    else:

        if is_staff:
            people_list = people_list.filter(Q(status__in=[STATUS_PUBLISHED, STATUS_PENDING])|Q(created_by=user))
        else:
            people_list = people_list.filter(Q(status__in=[STATUS_PUBLISHED])|Q(created_by=user, status__in=[STATUS_DRAFT, STATUS_PENDING]))


    query = people_list.query
    query.group_by = ['id']

    # SQL injection hack by developer for order MAX uptodate
    query.order_by.append('-is_deleted`, MAX(%s(COALESCE(`domain_statement.created, "1000-01-01"), COALESCE(domain_statement.changed, "1000-01-01")))' % settings.GREATEST_FUNCTION)

    query.order_by.reverse()

    return QuerySet(query=query, model=People)


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

@scache
def home(request):

    statement_list = statement_query_base(is_anonymous=True)

    meter_list = Meter.objects.order_by('order')


    meter_statement_count = Statement.objects.filter(status=STATUS_PUBLISHED).values('meter_id').annotate(count=Count('id'))
    meter_statement_count = dict([(meter['meter_id'], meter['count']) for meter in meter_statement_count])


    meter_statement_count = [(meter, meter_statement_count.get(meter.id) or 0) for meter in meter_list]

    hilight_statement_list = statement_list.filter(hilight=True).order_by('order', '-uptodate')

    statement_list = statement_list.exclude(hilight=True).order_by('-promote', '-uptodate')

    meter_statement_list = []

    if hilight_statement_list.count():
        hilight_title, created = Variable.objects.get_or_create(name='highlight_label')
        hilight_title = hilight_title.value or _('Highlight')
        meter_statement_list.append(({'title': hilight_title, 'permalink': 'highlight'}, hilight_statement_list))

    meter_statement_list.append(({'title': _('Latest'), 'permalink': 'latest'}, statement_list[0:4]))

    # Q 27
    for meter in meter_list:

        meter_statement = statement_list.filter(meter=meter)[0:5]
        meter_statement_list.append((meter, meter_statement))

    # Q 1
    tags_list = Tag.objects.usage_for_model(Statement, counts=True)
    tags_list.sort(key=Count, reverse=True)
    tags_list = tags_list[0:15]

    # Q 24
    people_list = people_query_base(is_anonymous=True)
    people_list = people_list.exclude(quoted_by__hilight=True)
    #people_list = people_list.exclude(id__in=people_statement_list)

    people_list = people_list[0:4]

    about, created = Variable.objects.get_or_create(name='about')


    return render(request, 'domain/home.html', {
        'meter_statement_count': meter_statement_count,
        'meter_statement_list': meter_statement_list,
        'tags_list': tags_list,
        'people_list': people_list,
        'contact_footer': render_to_string('contact_footer.txt'),
        'site_image': request.build_absolute_uri('%simages/site_image.jpg' % settings.STATIC_URL),
        'site_description': about.value
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
            if not people.created_by_id:
                people.created_by = request.user

            people.save()

            people.categories.clear()
            for category in form.cleaned_data['categories']:
                people.categories.add(category)

            message_success = get_success_message(people, is_new)

            if request.GET.get('_popup'):
                message_success = '<script type="text/javascript"> opener.dismissAddAnotherPopup(window, \'%s\', \'%s\'); </script>' % (people.id, people_render_reference(people))

            messages.success(request, message_success)
            warm_cache.delay({
                'SERVER_NAME': request.META['SERVER_NAME'],
                'SERVER_PORT': request.META['SERVER_PORT'],
                'wsgi.url_scheme': request.META['wsgi.url_scheme']
            })


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
@scache
def people_detail(request, people_permalink, meter_permalink=None):

    people = get_object_or_404(People, permalink=people_permalink)

    meter_list = Meter.objects.all().order_by('order')
    meter_statement_count = [(meter, meter.statement_set.filter(status=STATUS_PUBLISHED, quoted_by=people).count()) for meter in meter_list]

    statement_list = statement_query_base(request.user.is_anonymous(), request.user.is_staff, request.user)
    statement_list = statement_list.filter(Q(quoted_by=people)|Q(relate_peoples=people)).order_by('-uptodate')

    query = statement_list.query
    query.group_by = ['id']
    statement_list = QuerySet(query=query, model=Statement)

    request_meter = None
    if meter_permalink:
        request_meter = get_object_or_404(Meter, permalink=meter_permalink)
        statement_list = statement_list.filter(meter=request_meter)

    statement_list = pagination_build_query(request, statement_list, 5)

    people_list = people_query_base(is_anonymous=True)
    people_list = people_list.exclude(id=people.id)

    people_list = people_list[0:2]


    return render(request, 'domain/people_detail.html', {
        'people': people,
        'meter_statement_count': meter_statement_count,
        'statement_list': statement_list,
        'people_list': people_list,
        'request_meter': request_meter
    })


@scache
def people_list(request):

    category = request.GET.get('category')
  

    people_list = people_query_base(category, request.user.is_anonymous(), request.user.is_staff, request.user)
    people_list = pagination_build_query(request, people_list, 9)

    category_list = PeopleCategory.objects.all()

    if category and category.lower() != 'all':
        category = PeopleCategory.objects.get(permalink=category)

    return render(request, 'domain/people_list.html', {
        'people_list': people_list,
        'category_list': category_list,
        'request_category': category

    })



# =============================
# Meter
# =============================

@statistic
@scache
def meter_detail(request, meter_permalink=None):

    meter_list = Meter.objects.all().order_by('order')

    if not meter_permalink:
        meter = meter_list[0]
    else:
        meter = get_object_or_404(Meter, permalink=meter_permalink)

    statement_list = statement_query_base(request.user.is_anonymous(), request.user.is_staff, request.user)
    statement_list = statement_list.filter(meter=meter).order_by('-uptodate')

    statement_list = pagination_build_query(request, statement_list, 10)
    people_statement_list = [statement.quoted_by.id for statement in statement_list]
    people_statement_list = list(set(people_statement_list))

    people_list = people_query_base()
    people_list = people_list.exclude(id__in=people_statement_list)

    people_limit = len(statement_list)
    people_list = people_list[0:people_limit]



    return render(request, 'domain/meter_detail.html', {
        'request_meter': meter,
        'meter_list': meter_list,
        'statement_list': statement_list,
        'people_list': people_list
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


            warm_cache.delay({
                'SERVER_NAME': request.META['SERVER_NAME'],
                'SERVER_PORT': request.META['SERVER_PORT'],
                'wsgi.url_scheme': request.META['wsgi.url_scheme']
            })

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
@scache
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


@scache
def topic_list(request):
    return HttpResponse('Fixed me !!')


# =============================
# Topic Revision
# =============================

@scache
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
            if not statement.created_by_id:
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


            # Generate card from selenium capture screen
            url = request.build_absolute_uri(reverse('statement_item', args=[statement.id]))
            filename = 'statement-card-%s.png' % statement.id
            generate_statement_card.delay(url, filename)

            warm_cache.delay({
                'SERVER_NAME': request.META['SERVER_NAME'],
                'SERVER_PORT': request.META['SERVER_PORT'],
                'wsgi.url_scheme': request.META['wsgi.url_scheme']
            })

            return redirect('statement_edit', statement.id)
    else:
        initial = {
            'permalink': statement.permalink,
            'quote': statement.quote,
            'short_detail': statement.short_detail,
            'status': statement.status,
            'quoted_by': statement.quoted_by_id,
            'source': statement.source,
            'topic': statement.topic_id,
            'tags': statement.tags,
            'meter': statement.meter_id or Meter.objects.get(permalink='unverifiable').id,
            'hilight': statement.hilight,
            'promote': statement.promote,
        }

        if statement.id:
            initial['relate_statements'] = statement.relate_statements.all()
            initial['relate_peoples'] = statement.relate_peoples.all()
        else:
            initial['status'] = process_status(request.user, initial['status'], True)

        form = StatementEditForm(statement, Statement, initial=initial)

        reference_formset = ReferenceFormSet(initial=statement.references, prefix='references')

    hilight_label, created = Variable.objects.get_or_create(name='highlight_label')
    hilight_label = hilight_label.value or _('Highlight')

    return render(request, 'domain/statement_form.html', {
        'form': form,
        'reference_formset': reference_formset,
        'hilight_label': hilight_label
    })


@login_required
def statement_edit(request, statement_id=None):

    statement = get_object_or_404(Statement, id=statement_id)
    return statement_create(request, statement)


@statistic
@scache
def statement_detail(request, statement_permalink):

    statement = get_object_or_404(Statement, permalink=statement_permalink)
    try:
        topicrevision = TopicRevision.objects.filter(origin=statement.topic).latest('id')
    except TopicRevision.DoesNotExist:
        topicrevision = None

    if not statement.changed:
        statement.changed = statement.created


    # Generate card
    card_dir = '%s/card/statement' % settings.MEDIA_ROOT
    filename = 'statement-card-%s.png' % statement.id
    path = '%s/%s' % (card_dir, filename)

    if not os.path.exists(path):
        url = request.build_absolute_uri(reverse('statement_item', args=[statement.id]))
        #generate_statement_card.delay(url, filename)

    return render(request, 'domain/statement_detail.html', {
        'statement': statement,
        'topic': topicrevision,
        'meter_list': Meter.objects.all().order_by('order'),
        'meter_image': statement.meter.image_medium_text.thumbnail_500x500(upscale=True),
        'people_image': statement.quoted_by.image.thumbnail_500x500(upscale=True, crop='center'),
        'card_image': request.build_absolute_uri('%scard/statement/%s' % (settings.MEDIA_URL, filename)),
        'card_width': settings.CARD_WIDTH,
        'display_statement_revisions': settings.DISPLAY_STATEMENT_REVISIONS
    })

@scache
def statement_item(request, statement_id):

    print [s.id for s in Statement.objects.all()]
    statement = get_object_or_404(Statement, id=statement_id)

    return render(request, 'share/statement_item.html', {'statement': statement, 'card_width': settings.CARD_WIDTH})


@scache
def statement_topicrevision_detail(request, statement_permalink, topicrevision_id):

    statement = get_object_or_404(Statement, permalink=statement_permalink)
    topicrevision = get_object_or_404(TopicRevision, id=topicrevision_id)

    if not statement.changed:
        statement.changed = statement.created

    return render(request, 'domain/statement_detail.html', {
        'statement': statement,
        'topic': topicrevision,
        'meter_list': Meter.objects.all().order_by('order')
    })


@scache
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
        'tags_list': Tag.objects.all()[0:30],
        'request_tags': tags
    })


@scache
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

    item_list = Statement.objects.all().order_by('order', '-created', '-id').filter(hilight=True).exclude(status=STATUS_DRAFT)
    table = SortableStatementTable(item_list)
    RequestConfig(request).configure(table)


    if request.method == 'POST':
        for (name, value) in request.POST.items():
            try:
                id = int(name.replace('order-id-', ''))
                order = int(value)
                statement = Statement.objects.get(id=id)
                statement.order = order
                statement.save()
            except ValueError:
                pass
        messages.success(request, _('Your %s settings has been updated.') % _('order'))
        return redirect('manage_hilight_statement')

    return render(request, 'manage.html', {
        'table': table,
        'page_title': _('Manage Highlight Statements'),
        'sortable': True
    })


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

    from django.utils import translation

    return render(request, 'manage.html', {'table': table, 'page_title': _('Manage All People')})


@staff_member_required
def manage_information(request):

    if request.method == 'POST':
        form = InformationForm(request.POST)
        if form.is_valid():

            set_default_value('highlight_label', form.cleaned_data['highlight_label'])
            set_default_value('about', form.cleaned_data['about'])
            set_default_value('contact', form.cleaned_data['contact'])
            set_default_value('contact_footer', form.cleaned_data['contact_footer'])

    else:

        highlight_label, created = Variable.objects.get_or_create(name='highlight_label')
        about, created           = Variable.objects.get_or_create(name='about')
        contact, created         = Variable.objects.get_or_create(name='contact')
        contact_footer, created  = Variable.objects.get_or_create(name='contact_footer')

        initial = {
            'highlight_label': highlight_label.value,
            'about': about.value,
            'contact': contact.value,
            'contact_footer': contact_footer.value
        }
        form = InformationForm(initial=initial)

    return render(request, 'manage_information.html', {'form': form})

def maintenance_mode(request):
    return render(request, 'maintenance_mode.html')
