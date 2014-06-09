from ckeditor.widgets import CKEditorWidget
from django import forms
from django.forms import widgets
from common.constants import STATUS_CHOICES
import files_widget
from common.forms import PermalinkForm
from domain.models import PeopleCategory, People


class PeopleEditForm(PermalinkForm):

    permalink = forms.CharField()

    categories = forms.ModelMultipleChoiceField(queryset=PeopleCategory.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'id': 'id_categories'}))

    first_name = forms.CharField(max_length=30, widget=forms.TextInput())
    last_name = forms.CharField(max_length=30, widget=forms.TextInput())

    occupation = forms.CharField(required=False, max_length=128, widget=forms.TextInput())
    description = forms.CharField(required=False, widget=CKEditorWidget(config_name='minimal'))
    homepage_url = forms.CharField(required=False, max_length=255, widget=forms.TextInput())

    image = files_widget.forms.FilesFormField(required=False, fields=(forms.CharField(required=False), forms.CharField(required=False), forms.CharField(required=False), ), widget=files_widget.forms.widgets.ImageWidget())

    status = forms.ChoiceField(required=False, widget=forms.RadioSelect(attrs={'id': 'id_status'}), choices=STATUS_CHOICES)


class TopicEditForm(PermalinkForm):

    permalink = forms.CharField()

    title = forms.CharField(max_length=30, widget=forms.TextInput())
    description = forms.CharField(required=False, widget=CKEditorWidget(config_name='default'))

    without_revision = forms.NullBooleanField(widget=forms.CheckboxInput())



'''
class ReferenceWidget(widgets.MultiWidget):

    def __init__(self, attrs=None):
        widget = (forms.TextInput(), forms.URLInput())
        super(ReferenceWidget, self).__init__(widget, attrs=attrs)

    def decompress(self, value):

        if value and type(value) == dict:
            return [value['title'], value['url']]
        return [None, None]


class ReferenceField(forms.MultiValueField):
    widget = ReferenceWidget

    def __init__(self, required=True, widget=None, label=None, initial=None, help_text=None):

        field = (forms.CharField(), forms.URLField())
        super(ReferenceField, self).__init__(required=required, fields=field, widget=widget, label=label, initial=initial, help_text=help_text)

    def compress(self, data_list):
        return {'title': data_list[0], 'url': data_list[1]}


class MultiReferenceWidget(widgets.MultiWidget):

    def __init__(self, attrs=None):
        widget = (ReferenceWidget(), ReferenceWidget())
        super(MultiReferenceWidget, self).__init__(widget, attrs=attrs)

    def decompress(self, value):

        print value

        if value and type(value) == list:
            return value
        return [None, None]


class MultiReferenceField(forms.MultiValueField):
    widget = MultiReferenceWidget

    def __init__(self, required=True, widget=None, label=None, initial=None, help_text=None):

        field = (ReferenceField(), ReferenceField())
        super(MultiReferenceField, self).__init__(required=required, fields=field, widget=widget, label=label, initial=initial, help_text=help_text)

    def compress(self, data_list):
        return data_list
'''


class ReferenceForm(forms.Form):
    title = forms.CharField(required=False, widget=forms.TextInput())
    url = forms.URLField(required=False, widget=forms.URLInput())


class StatementEditForm(PermalinkForm):

    permalink = forms.CharField()

    quoted_by = forms.ModelChoiceField(queryset=People.objects.all(), widget=forms.RadioSelect(attrs={'id': 'id_quoted_by'}))
    quote = forms.CharField(widget=CKEditorWidget(config_name='bold'))

    title = forms.CharField(required=False, max_length=30, widget=forms.TextInput())
    description = forms.CharField(required=False, widget=CKEditorWidget(config_name='default'))

    #references = MultiReferenceField()

    status = forms.ChoiceField(required=False, widget=forms.RadioSelect(attrs={'id': 'id_status'}), choices=STATUS_CHOICES)

