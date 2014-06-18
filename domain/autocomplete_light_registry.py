import autocomplete_light
from django.db.models.query import QuerySet

from common.functions import people_render_reference, topic_render_reference
from models import People, Topic, TopicRevision, Statement


class PeopleAutocomplete(autocomplete_light.AutocompleteModelBase):

    choices = People.objects.filter()
    search_fields = ['first_name', 'last_name', 'permalink']

    def choice_label(self, choice):
        return people_render_reference(choice)


    def choice_html(self, choice):

        return self.choice_html_format % (
            self.choice_value(choice),
            self.choice_label(choice))


def get_default_topic_quesrset():

    query = TopicRevision.objects.all().query
    query.group_by = ['origin_id']
    results = QuerySet(query=query, model=TopicRevision)

    return results


class TopicAutocomplete(autocomplete_light.AutocompleteModelBase):

    choices = get_default_topic_quesrset()
    search_fields = ['title']

    def choice_value(self, choice):

        return choice.origin.id

    def choice_label(self, choice):
        return topic_render_reference(choice.origin)


    def choice_html(self, choice):

        return self.choice_html_format % (
            self.choice_value(choice),
            self.choice_label(choice))


autocomplete_light.register(People, PeopleAutocomplete)
autocomplete_light.register(Topic, TopicAutocomplete)
