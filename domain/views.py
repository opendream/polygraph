from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from common.constants import STATUS_PUBLISHED
from common.functions import people_render_reference, topic_render_reference, statement_render_reference
from domain.forms import PeopleEditForm, TopicEditForm, StatementEditForm, ReferenceForm
from domain.models import People, Topic, Statement, Meter


def home(request):

    return render(request, 'domain/home.html', {})


def statement_list(request):

    return render(request, 'domain/statement_list.html', {})

def statement_detail(request, statement_permalink):

    return render(request, 'domain/statement_detail.html', {statement_permalink: statement_permalink})


# Staff form ===========================================================================



@login_required
def people_create(request, people=None):

    if not people:
        people = People()
        message_success = _('New %s has been created. View this %s <a href="%s">here</a>.') % (_('people'), _('people'), '#')
    else:
        message_success = _('Your %s settings has been updated. View this %s <a href="%s">here</a>.') % (_('people'), _('people'), '#')


    if request.method == 'POST':
        form = PeopleEditForm(people, People, request.POST)
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
            people.save()

            people.categories.clear()
            for category in form.cleaned_data['categories']:
                people.categories.add(category)


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



@login_required
def topic_create(request, topic=None):

    if not topic:
        topic = Topic()
        message_success = _('New %s has been created. View this %s <a href="%s">here</a>.') % (_('topic'), _('topic'), '#')
    else:
        message_success = _('Your %s settings has been updated. View this %s <a href="%s">here</a>.') % (_('topic'), _('topic'), '#')


    if request.method == 'POST':
        form = TopicEditForm(topic, Topic, request.POST)
        if form.is_valid():
            topic.title = form.cleaned_data['title']
            topic.description = form.cleaned_data['description']
            topic.created_by = request.user

            as_revision = bool(form.cleaned_data['as_revision'])
            without_revision = not as_revision

            topic.save(without_revision=without_revision)

            if request.GET.get('_popup'):
                message_success = '<script type="text/javascript"> opener.dismissAddAnotherPopup(window, \'%s\', \'%s\'); </script>' % (topic.id, topic_render_reference(topic))

            messages.success(request, message_success)

            if request.GET.get('_inline') or request.POST.get('_inline'):
                form.inst = topic
            else:
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
def statement_create(request, statement=None):

    if not statement:
        statement = Statement()
        message_success = _('New %s has been created. View this %s <a href="%s">here</a>.') % (_('statement'), _('statement'), '#')
    else:
        message_success = _('Your %s settings has been updated. View this %s <a href="%s">here</a>.') % (_('statement'), _('statement'), '#')

    ReferenceFormSet = formset_factory(ReferenceForm, extra=2, can_delete=True)


    if request.method == 'POST':

        form = StatementEditForm(statement, Statement, request.POST)
        reference_formset = ReferenceFormSet(request.POST, prefix='references')

        if form.is_valid() and reference_formset.is_valid():
            statement.permalink = form.cleaned_data['permalink']
            statement.quote = form.cleaned_data['quote']
            statement.created_by = request.user
            statement.quoted_by_id = form.cleaned_data['quoted_by'].id
            statement.topic_id = form.cleaned_data['topic'].id if form.cleaned_data['topic'] else None
            statement.tags = form.cleaned_data['tags']
            statement.meter_id = form.cleaned_data['meter'].id


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
            'topic': statement.topic_id,
            'tags': statement.tags,
            'meter': statement.meter_id or Meter.objects.get(permalink='unprovable').id
        }

        if statement.id:
            initial['relate_statements'] = statement.relate_statements.all()
            initial['relate_peoples'] = statement.relate_peoples.all()

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