import autocomplete_light
from django.core import urlresolvers
from django.core.exceptions import ImproperlyConfigured
from django.db.models.query import QuerySet

from common.functions import people_render_reference, topic_render_reference, statement_render_reference
from models import People, Topic, TopicRevision, Statement


class PeopleAutocomplete(autocomplete_light.AutocompleteModelBase):

    choices = People.objects.all().order_by('-id')
    search_fields = ['first_name', 'last_name', 'permalink']

    def choice_label(self, choice):
        return people_render_reference(choice)


    def choice_html(self, choice):

        return self.choice_html_format % (
            self.choice_value(choice),
            self.choice_label(choice))


def get_default_topic_queryset():

    query = TopicRevision.objects.all().order_by('-id').query
    query.group_by = ['origin_id']
    results = QuerySet(query=query, model=TopicRevision)


    return results


class TopicAutocomplete(autocomplete_light.AutocompleteModelBase):

    choices = get_default_topic_queryset()
    search_fields = ['title']

    def choices_for_values(self):
        """
        Return ordered choices which pk are in
        :py:attr:`~.base.AutocompleteInterface.values`.
        """
        assert self.choices is not None, 'choices should be a queryset'
        return self.order_choices(self.choices.filter(
            origin__id__in=self.values or []))

    def choices_for_request(self):
        """
        Return a queryset based on :py:attr:`choices` using options
        :py:attr:`split_words`, :py:attr:`search_fields` and
        :py:attr:`limit_choices`.
        """
        assert self.choices is not None, 'choices should be a queryset'
        assert self.search_fields, 'autocomplete.search_fields must be set'
        q = self.request.GET.get('q', '')
        exclude = self.request.GET.getlist('exclude')

        conditions = self._choices_for_request_conditions(q,
                self.search_fields)

        return self.order_choices(self.choices.filter(
            conditions).exclude(origin__id__in=exclude))[0:self.limit_choices]

    def choice_value(self, choice):

        return choice.origin.id

    def choice_label(self, choice):
        return topic_render_reference(choice.origin)


    def choice_html(self, choice):

        return self.choice_html_format % (
            self.choice_value(choice),
            self.choice_label(choice))


def get_default_statement_queryset():

    query = Statement.objects.all().order_by('-id').query
    query.group_by = ['id']
    results = QuerySet(query=query, model=Statement)

    return results

class StatementAutocomplete(autocomplete_light.AutocompleteModelBase):

    choices = get_default_statement_queryset()
    search_fields = ['quote', 'permalink', 'topic__topicrevision__title']

    def choice_label(self, choice):
        return statement_render_reference(choice)

    def choice_html(self, choice):

        return self.choice_html_format % (
            self.choice_value(choice),
            self.choice_label(choice))

    def get_absolute_url(self):
        """
        Return the absolute url for this autocomplete, using
        autocomplete_light_autocomplete url.
        """
        try:
            return '%s' % urlresolvers.reverse('autocomplete_light_autocomplete',
                args=(self.__class__.__name__,))
        except urlresolvers.NoReverseMatch as e:
            # Such error will ruin form rendering. It would be automatically
            # silenced because of e.silent_variable_failure=True, which is
            # something we don't want. Let's give the user a hint:
            raise ImproperlyConfigured("URL lookup for autocomplete '%s' "
                    "failed. Have you included autocomplete_light.urls in "
                    "your urls.py?" % (self.__class__.__name__,))


autocomplete_light.register(People, PeopleAutocomplete)
autocomplete_light.register(Topic, TopicAutocomplete)
autocomplete_light.register(Statement, StatementAutocomplete)
