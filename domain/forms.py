from ckeditor.widgets import CKEditorWidget
from django import forms
from django.core.validators import validate_slug
from django.utils.translation import ugettext_lazy as _

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

    permalink   = forms.CharField(max_length=255, validators=[validate_slug])

    first_name  = forms.CharField(max_length=30, widget=forms.TextInput())
    last_name   = forms.CharField(max_length=30, widget=forms.TextInput())

    occupation  = forms.CharField(required=False, max_length=128, widget=forms.TextInput())
    description = forms.CharField(required=False, widget=CKEditorWidget(config_name='minimal'))
    homepage_url = forms.CharField(required=False, max_length=255, widget=forms.TextInput())





