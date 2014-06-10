import autocomplete_light
from ckeditor.widgets import CKEditorWidget
from django import forms
from common.constants import STATUS_CHOICES, STATUS_PUBLISHED
from domain.autocomplete_light_registry import PeopleAutocomplete
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


class ReferenceForm(forms.Form):
    title = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control'}))


class StatementEditForm(PermalinkForm):

    permalink = forms.CharField()

    #quoted_by = forms.ModelChoiceField(queryset=People.objects.all(), widget=forms.RadioSelect(attrs={'id': 'id_quoted_by'}))
    quoted_by = forms.ModelChoiceField(
        queryset=People.objects.filter(status=STATUS_PUBLISHED),
        widget=autocomplete_light.ChoiceWidget(PeopleAutocomplete,
                                               attrs={'placeholder': 'Type people name', 'class': 'form-control'}


        )
    )


    quote = forms.CharField(widget=CKEditorWidget(config_name='bold'))

    title = forms.CharField(required=False, max_length=30, widget=forms.Textarea())
    description = forms.CharField(required=False, widget=CKEditorWidget(config_name='default'))

    #references = MultiReferenceField()

    status = forms.ChoiceField(required=False, widget=forms.RadioSelect(attrs={'id': 'id_status'}), choices=STATUS_CHOICES)

