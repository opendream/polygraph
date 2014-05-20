from django.contrib.auth.views import login, password_reset, password_reset_done
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from account.forms import EmailAuthenticationForm, ResetPasswordForm


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