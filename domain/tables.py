from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from django_tables2.utils import A, AttributeDict
from common.constants import STATUS_CHOICES
from common.functions import image_render
from common.templatetags.common_tags import do_format_abbr_date
from domain.models import Statement, People

import django_tables2 as tables

class SafeLinkColumn(tables.LinkColumn):
    def render_link(self, uri, text, attrs=None):

        attrs = AttributeDict(attrs if attrs is not None else
                              self.attrs.get('a', {}))
        attrs['href'] = uri
        html = '<a {attrs}>{text}</a>'.format(
            attrs=attrs.as_html(),
            text=text.encode('utf-8')
        )
        return mark_safe(html)

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

class OrderColum(tables.Column):
    def render(self, value):
        return mark_safe('<input type="text" value="%s" name=""/> ' % value)

class StatementTable(tables.Table):
    created_by = tables.Column(accessor='created_by.get_full_name', verbose_name=_('Writer'))
    quote = SafeLinkColumn('statement_edit', args=[A('id')], verbose_name=_('Quote'))
    topic = SafeLinkColumn('topic_edit', args=[A('topic.id')], accessor='topic.title', order_by='topic.topicrevision.title', verbose_name=_('Topic'))
    quoted_by = SafeLinkColumn('people_edit', args=[A('quoted_by.id')], accessor='quoted_by.get_full_name', verbose_name=_('Said by'), order_by='quoted_by.first_name')
    meter = tables.Column(accessor='meter.title', verbose_name=_('Meter'))
    status = StatusColumn(verbose_name=_('Status'))
    created = DateColumn(verbose_name=_('Created'))

    class Meta:
        model = Statement
        fields = ('created_by', 'quote', 'quoted_by', 'meter', 'topic', 'status', 'created')


class SortableStatementTable(StatementTable):
    order = tables.Column(verbose_name=_('Order'))
    id = tables.Column(visible=False)

    class Meta:
        fields = ('id', 'order', 'quote', 'quoted_by', 'meter', 'topic', 'status', 'created', 'created_by')

    def render_order(self, value, bound_row, record):
        return mark_safe('<input type="text" value="%s" name="order-id-%s" readonly /> ' % (value, bound_row['id']))


class MyStatementTable(StatementTable):

    class Meta:
        exclude = ('created_by', )


class PeopleTable(tables.Table):
    image = ImageColumn(verbose_name=_('Image'))
    name = SafeLinkColumn('people_edit', args=[A('id')], accessor='get_full_name', verbose_name=_('Name'))
    categories = MultipleColum(verbose_name=_('Categories'))
    status = StatusColumn(verbose_name=_('Status'))
    created = DateColumn(verbose_name=_('Created'))
    created_by = tables.Column(accessor='created_by.get_full_name', verbose_name=_('Writer'))

    class Meta:
        model = People
        fields = ('created_by', 'image', 'name', 'categories', 'status', 'created')

class SortablePeopleTable(PeopleTable):
    order = tables.Column(verbose_name=_('Order'))
    id = tables.Column(visible=False)

    class Meta:
        fields = ('id', 'order', 'image', 'name', 'categories', 'status', 'created', 'created_by')

    def render_order(self, value, bound_row, record):
        return mark_safe('<input type="text" value="%s" name="order-id-%s" readonly /> ' % (value, bound_row['id']))

class MyPeopleTable(PeopleTable):

    class Meta:
        exclude = ('created_by', )
