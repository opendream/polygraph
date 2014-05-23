from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.utils.translation import ugettext_lazy as _


class EmailAuthenticationForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    remember_me = forms.NullBooleanField()

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(EmailAuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')


        if email and password:
            self.user_cache = authenticate(username=email, password=password)

            if self.user_cache is None:
                raise forms.ValidationError(_('Please, enter correct email/username and password.'))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_('This account not activated.'))

        return self.cleaned_data


    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(max_length=75)

    def clean_email(self):

        email = self.cleaned_data.get('email')

        UserModel = get_user_model()

        try:
            UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            raise forms.ValidationError(_('Your email address is not registered.'))

        return self.cleaned_data


class AccountEditForm(forms.Form):

    username    = forms.CharField(max_length=75)
    email       = forms.EmailField(max_length=75)
    password    = forms.CharField(required=False, max_length=128, widget=forms.PasswordInput())
    password2   = forms.CharField(required=False, max_length=128, widget=forms.PasswordInput())
    first_name  = forms.CharField(required=False, max_length=30, widget=forms.TextInput())
    last_name   = forms.CharField(required=False, max_length=30, widget=forms.TextInput())

    occupation  = forms.CharField(required=False, max_length=128, widget=forms.TextInput())
    description = forms.CharField(required=False, widget=CKEditorWidget(config_name='minimal'))
    homepage_url = forms.CharField(required=False, max_length=255, widget=forms.TextInput())

    def __init__(self, required_password=False, request=None,  *args, **kwargs):
        super(AccountEditForm, self).__init__(*args, **kwargs)

        self.request = request

        if required_password:
            self.fields['password'].required = True
            self.fields['password2'].required = True


    def clean_username(self):
        username = self.cleaned_data.get('username', '')

        if get_user_model().objects.filter(username=username).exclude(id=self.request.user.id).count() > 0:
            raise forms.ValidationError(_('This username is already in use.'))
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', '')

        if get_user_model().objects.filter(email=email).exclude(id=self.request.user.id).count() > 0:
            raise forms.ValidationError(_('This email is already in use.'))
        return email

    def clean_password2(self):
        password = self.cleaned_data.get('password', '')
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError(_('Password mismatch.'))
        return password2
