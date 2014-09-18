import autocomplete_light
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.utils.translation import ugettext_lazy as _

from common.constants import STATUS_CHOICES, STATUS_PUBLISHED

from domain.autocomplete_light_registry import PeopleAutocomplete, TopicAutocomplete, StatementAutocomplete
import files_widget
from common.forms import PermalinkForm, CommonForm
from domain.models import PeopleCategory, People, Topic, Meter, Statement

from tagging.forms import TagField
from tagging_autocomplete_tagit.widgets import TagAutocompleteTagIt

class PeopleEditForm(PermalinkForm):

    permalink = forms.CharField()

    categories = forms.ModelMultipleChoiceField(queryset=PeopleCategory.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'id': 'id_categories'}))

    first_name = forms.CharField(max_length=255, widget=forms.TextInput())
    last_name = forms.CharField(max_length=255, widget=forms.TextInput())

    occupation = forms.CharField(required=False, max_length=255, widget=forms.TextInput())
    summary = forms.CharField(required=False, widget=forms.Textarea())
    description = forms.CharField(required=False, widget=CKEditorWidget(config_name='minimal'))
    homepage_url = forms.CharField(required=False, max_length=255, widget=forms.TextInput())

    image = files_widget.forms.FilesFormField(required=False, fields=(forms.CharField(required=False), forms.CharField(required=False), forms.CharField(required=False), ), widget=files_widget.forms.widgets.ImageWidget())

    status = forms.ChoiceField(required=False, widget=forms.RadioSelect(attrs={'id': 'id_status'}), choices=STATUS_CHOICES)


class TopicEditForm(CommonForm):

    title = forms.CharField(max_length=255, widget=forms.TextInput())
    description = forms.CharField(required=False, widget=CKEditorWidget(config_name='default'))

    as_revision = forms.NullBooleanField(widget=forms.CheckboxInput(attrs={'chacked': 'checked'}))


class ReferenceForm(forms.Form):
    title = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control first', 'placeholder': _('Title')}))
    url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control last', 'placeholder': _('URL')}))


class StatementEditForm(PermalinkForm):

    permalink = forms.CharField()

    quote = forms.CharField(widget=CKEditorWidget(config_name='bold'))

    short_detail = forms.CharField(required=False, widget=CKEditorWidget(config_name='minimal'))

    quoted_by = forms.ModelChoiceField(
        queryset=People.objects.all(),
        widget=autocomplete_light.ChoiceWidget(PeopleAutocomplete,
            attrs={'placeholder': _('Type for search people by name'), 'class': 'form-control'}
        )
    )

    source = forms.CharField(required=False, widget=forms.TextInput())

    topic = forms.ModelChoiceField(
        required=False,
        queryset=Topic.objects.all(),
        widget=autocomplete_light.ChoiceWidget(TopicAutocomplete,
            attrs={'placeholder': _('Type for search topic by title'), 'class': 'form-control'}
        )
    )

    tags = TagField(required=False, widget=TagAutocompleteTagIt(max_tags=False))

    meter = forms.ModelChoiceField(
        required=True,
        queryset=Meter.objects.all(),
        empty_label=None,
        widget=forms.RadioSelect(attrs={'id': 'id_meter'})
    )

    relate_statements = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Statement.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(StatementAutocomplete,
            attrs={'placeholder': _('Type for search statement by quote or topic title'), 'class': 'form-control'}
        )
    )

    relate_peoples = forms.ModelMultipleChoiceField(
        required=False,
        queryset=People.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(PeopleAutocomplete,
            attrs={'placeholder': _('Type for search people by name'), 'class': 'form-control'}
        )
    )

    status = forms.ChoiceField(required=False, widget=forms.RadioSelect(attrs={'id': 'id_status'}), choices=STATUS_CHOICES)
    hilight = forms.NullBooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'id_hilight'}))
    promote = forms.NullBooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'id_promote'}))

class InformationForm(forms.Form):

    highlight_label = forms.CharField(required=False, max_length=255, widget=forms.TextInput())
    about = forms.CharField(required=False, widget=CKEditorWidget(config_name='default'))
    contact = forms.CharField(required=False, widget=CKEditorWidget(config_name='default'))
    contact_footer = forms.CharField(required=False, widget=CKEditorWidget(config_name='default'))