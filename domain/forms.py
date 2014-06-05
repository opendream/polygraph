from ckeditor.widgets import CKEditorWidget
from django import forms
from common.constants import STATUS_CHOICES
import files_widget
from common.forms import PermalinkForm
from domain.models import PeopleCategory


class PeopleEditForm(PermalinkForm):

    permalink = forms.CharField()

    categories = forms.ModelMultipleChoiceField(queryset=PeopleCategory.objects.all(), widget=forms.CheckboxSelectMultiple())

    first_name = forms.CharField(max_length=30, widget=forms.TextInput())
    last_name = forms.CharField(max_length=30, widget=forms.TextInput())

    occupation = forms.CharField(required=False, max_length=128, widget=forms.TextInput())
    description = forms.CharField(required=False, widget=CKEditorWidget(config_name='minimal'))
    homepage_url = forms.CharField(required=False, max_length=255, widget=forms.TextInput())

    image = files_widget.forms.FilesFormField(required=False, fields=(forms.CharField(required=False), forms.CharField(required=False), forms.CharField(required=False), ), widget=files_widget.forms.widgets.ImageWidget())

    status = forms.ChoiceField(required=False, widget=forms.RadioSelect, choices=STATUS_CHOICES)


class TopicEditForm(PermalinkForm):

    permalink = forms.CharField()

    title = forms.CharField(max_length=30, widget=forms.TextInput())
    description = forms.CharField(required=False, widget=CKEditorWidget(config_name='default'))

    without_revision = forms.NullBooleanField(widget=forms.CheckboxInput())



class StatementEditForm(PermalinkForm):

    permalink = forms.CharField()

    quoted_by = forms.CharField(widget=CKEditorWidget(config_name='default'))
    quote = forms.CharField(widget=CKEditorWidget(config_name='default'))

    title = forms.CharField(required=False, max_length=30, widget=forms.TextInput())
    description = forms.CharField(required=False, widget=CKEditorWidget(config_name='default'))
    references = forms.CharField(required=False, widget=forms.Textarea)


