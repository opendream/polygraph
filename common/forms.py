from django import forms
from django.core import validators
from django.utils.translation import ugettext_lazy as _

import re

class PermalinkForm(forms.Form):

    PERMALINK_FIELDS = ['permalink']

    def __init__(self, inst=None, model=None, *args, **kwargs):
        super(PermalinkForm, self).__init__(*args, **kwargs)
        self.inst = inst
        self.model = model

        for field_name in self.PERMALINK_FIELDS:
            self.fields[field_name].max_length = 255
            self.fields[field_name].validators = [validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid permalink.'), 'invalid')]
            self.fields[field_name].help_text = _('Required unique 30 characters or fewer. Letters, numbers and '
                                                  './@/+/-/_ characters')

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