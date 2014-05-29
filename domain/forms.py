from ckeditor.widgets import CKEditorWidget
from django import forms
from django.utils.translation import ugettext_lazy as _
from topnotchdev import files_widget
from common.forms import PermalinkForm


class PeopleEditForm(PermalinkForm):

    permalink = forms.CharField()

    first_name = forms.CharField(max_length=30, widget=forms.TextInput())
    last_name = forms.CharField(max_length=30, widget=forms.TextInput())

    occupation = forms.CharField(required=False, max_length=128, widget=forms.TextInput())
    description = forms.CharField(required=False, widget=CKEditorWidget(config_name='minimal'))
    homepage_url = forms.CharField(required=False, max_length=255, widget=forms.TextInput())

    image = files_widget.forms.FilesFormField(required=False, fields=(forms.CharField(required=False), forms.CharField(required=False), forms.CharField(required=False), ), widget=files_widget.forms.widgets.ImageWidget())
    #image = files_widget.forms.FilesFormField(required=False, fields=(forms.HiddenInput(), forms.HiddenInput(), forms.HiddenInput(), ), widget=files_widget.forms.widgets.ImageWidget())



