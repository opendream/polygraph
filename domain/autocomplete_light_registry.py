import autocomplete_light
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from common.constants import STATUS_PUBLISHED
from common.functions import people_render_reference
from models import People

class PeopleAutocomplete(autocomplete_light.AutocompleteModelBase):

    choices = People.objects.filter(status=STATUS_PUBLISHED)
    search_fields = ['first_name', 'last_name', 'permalink']

    def choice_label(self, choice):
        return people_render_reference(choice)


    def choice_html(self, choice):

        return self.choice_html_format % (
            self.choice_value(choice),
            self.choice_label(choice))

autocomplete_light.register(People, PeopleAutocomplete)