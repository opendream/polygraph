from django.contrib.auth.views import login
from django.shortcuts import redirect
from account.forms import EmailAuthenticationForm


def account_login(request):
    if request.user.is_authenticated():
        return redirect('domain_home')

    return login(request, authentication_form=EmailAuthenticationForm,
        template_name='account/login.html')