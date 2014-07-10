
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from django_tables2.utils import A
from common.constants import STATUS_CHOICES
from common.functions import image_render
from common.templatetags.common_tags import do_format_abbr_date
from domain.models import Statement, People

import django_tables2 as tables

class SafeLinkColumn(tables.LinkColumn):
    def render(self, value, record, bound_column):
        value = mark_safe(value)
        return super(SafeLinkColumn, self).render(value, record, bound_column)

class ImageColumn(tables.Column):
    def render(self, value):
        return mark_safe(image_render(value, '80x80'))

class StatusColumn(tables.Column):
    def render(self, value):
        return dict(STATUS_CHOICES)[value]

class DateColumn(tables.Column):
    def render(self, value):
        return do_format_abbr_date(value)

class MultipleColum(tables.Column):
    def render(self, value):
        return ', '.join([ v.__unicode__() for v in value.all()])


class StatementTable(tables.Table):
    created_by = tables.Column(accessor='created_by.get_full_name', verbose_name=_('Writer'))
    quote = SafeLinkColumn('statement_edit', args=[A('id')])
    topic = SafeLinkColumn('topic_edit', args=[A('id')], accessor='topic.title')
    quoted_by = SafeLinkColumn('people_edit', args=[A('id')], accessor='quoted_by.get_full_name', verbose_name=_('Said by'))
    meter = tables.Column(accessor='meter.title', verbose_name=_('Meter'))
    status = StatusColumn()
    created = DateColumn()

    class Meta:
        model = Statement
        fields = ('created_by', 'quote', 'quoted_by', 'meter', 'topic', 'status', 'created')


class MyStatementTable(StatementTable):

    class Meta:
        exclude = ('created_by', )


class PeopleTable(tables.Table):
    created_by = tables.Column(accessor='created_by.get_full_name', verbose_name=_('Writer'))
    image = ImageColumn()
    name = SafeLinkColumn('people_edit', args=[A('id')], accessor='get_full_name', verbose_name=_('Name'))
    categories = MultipleColum()
    status = StatusColumn()
    created = DateColumn()

    class Meta:
        model = People
        fields = ('created_by', 'image', 'name', 'categories', 'status', 'created')


class MyPeopleTable(PeopleTable):

    class Meta:
        exclude = ('created_by', )
