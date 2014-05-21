from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import login, password_reset, password_reset_done
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.http import base36_to_int
from account.forms import EmailAuthenticationForm, ResetPasswordForm, AccountEditForm


def account_login(request):

    if request.method == 'POST' and not request.POST.get('remember_me', None): # No unit test
        request.session.set_expiry(0) # No unit test

    if request.user.is_authenticated():
        return redirect('domain_home')

    return login(request, authentication_form=EmailAuthenticationForm,
        template_name='account/login.html')


def account_reset_password(request):
    if request.user.is_authenticated():
        return HttpResponse('access denied', status=403)

    return password_reset(request,
        template_name='account/password_reset_form.html',
        email_template_name='account/email/password_reset_email.html',
        subject_template_name='account/email/password_reset_email_subject.txt',
        password_reset_form=ResetPasswordForm,
        post_reset_redirect=reverse('account_reset_password_done'),
    )



def account_reset_password_done(request):
    return password_reset_done(request,
        template_name='account/password_reset_done.html'
    )


def account_reset_password_confirm(request, uidb36=None, token=None, email_setting=False):

    UserModel = get_user_model()

    try:
        uid_int = base36_to_int(uidb36)
        user = UserModel.objects.get(id=uid_int)
    except (ValueError, UserModel.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user_authen = authenticate(username=user.username, ignore_password=True)
        auth_login(request, user_authen)
        return redirect(reverse('account_edit') + '?reset_password=True')
    else:
        return HttpResponse('invalid link', status=404)


@login_required
def account_edit(request):

    required_password = request.GET.get('reset_password')

    if request.method == 'POST':
        form = AccountEditForm(required_password, request.POST)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']

            password = form.cleaned_data.get('password')
            if password:
                request.user.set_password(password)
            request.user.save()

            messages.success(request, _('Your account profile has been updated.'))

            return redirect('domain_home')
    else:
        form = AccountEditForm(required_password, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        })

    return render(request, 'account/edit.html', {
        'form': form,
        'reset_password': required_password,
    })