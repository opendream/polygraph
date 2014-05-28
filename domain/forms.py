import re
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from topnotchdev import files_widget


class PermalinkForm(forms.Form):

    PERMALINK_FIELDS = ['permalink']

    def __init__(self, inst=None, model=None, *args, **kwargs):
        super(PermalinkForm, self).__init__(*args, **kwargs)
        self.inst = inst
        self.model = model


    def clean(self):

        cleaned_data = super(PermalinkForm, self).clean()

        for field_name in self.PERMALINK_FIELDS:
            permalink = cleaned_data.get(field_name, '')

            if self.model.objects.filter(**{field_name: permalink}).exclude(id=self.inst.id).count() > 0:
                self._errors[field_name] = [_('This %s is already in use.') % field_name]

        return cleaned_data

    def is_new(self):

        if self.inst and self.inst.id:
            return False

        return True


class PeopleEditForm(PermalinkForm):

    permalink = forms.CharField(
        max_length=255,
        validators=[validators.RegexValidator(re.compile('^[\w.+-]+$'), _('Enter a valid permalink.'), 'invalid')],
        help_text=_('Required unique 30 characters or fewer. Letters, numbers and '
                    './+/-/_ characters')
    )

    first_name = forms.CharField(max_length=30, widget=forms.TextInput())
    last_name = forms.CharField(max_length=30, widget=forms.TextInput())

    occupation = forms.CharField(required=False, max_length=128, widget=forms.TextInput())
    description = forms.CharField(required=False, widget=CKEditorWidget(config_name='minimal'))
    homepage_url = forms.CharField(required=False, max_length=255, widget=forms.TextInput())

    image = files_widget.forms.FilesFormField(required=False, fields=(forms.CharField(required=False), forms.CharField(required=False), forms.CharField(required=False), ), widget=files_widget.forms.widgets.ImageWidget())




