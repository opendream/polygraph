import autocomplete_light
from common.constants import STATUS_PUBLISHED
from models import People

class PeopleAutocomplete(autocomplete_light.AutocompleteModelBase):

    choices = People.objects.filter(status=STATUS_PUBLISHED)
    search_fields=['first_name', 'last_name', 'permalink']

    def choice_label(self, choice):
        return '<img src="%s" /> %s' % (choice.image.thumbnail_100x100().url, choice.get_full_name())


    def choice_html(self, choice):

        print choice

        return self.choice_html_format % (
            self.choice_value(choice),
            self.choice_label(choice))

autocomplete_light.register(People, PeopleAutocomplete)