from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from domain.forms import PeopleEditForm
from domain.models import People


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
        message_success = _('Your settings has been updated.')


    if request.method == 'POST':
        form = PeopleEditForm(people, People, request.POST)
        if form.is_valid():
            people.permalink = form.cleaned_data['permalink']
            people.first_name = form.cleaned_data['first_name']
            people.last_name = form.cleaned_data['last_name']
            people.occupation = form.cleaned_data['occupation']
            people.description = form.cleaned_data['description']
            people.homepage_url = form.cleaned_data['homepage_url']
            people.save()

            messages.success(request, message_success)

            return redirect('people_edit', people.id)
    else:

        form = PeopleEditForm(people, People, initial={
            'permalink': people.permalink,
            'first_name': people.first_name,
            'last_name': people.last_name,
            'occupation': people.occupation,
            'description': people.description,
            'homepage_url': people.homepage_url
        })

    return render(request, 'domain/people_form.html', {
        'form': form
    })


@login_required
def people_edit(request, people_id=None):

    people = get_object_or_404(People, pk=people_id)
    return people_create(request, people)

