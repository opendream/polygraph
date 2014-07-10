
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

import django_tables2 as tables
from common.constants import STATUS_CHOICES
from common.functions import image_render
from common.templatetags.common_tags import do_format_abbr_date
from domain.models import Statement, People

class SafeColumn(tables.Column):
    def render(self, value):
        return mark_safe(value)

class ImageColumn(tables.Column):
    def render(self, value):
        return mark_safe(image_render(value, '80x80'))

class StatusColumn(tables.Column):
    def render(self, value):
        return dict(STATUS_CHOICES)[value]

class DateColumn(tables.Column):
    def render(self, value):
        return do_format_abbr_date(value)


class StatementTable(tables.Table):
    created_by = tables.Column(accessor='created_by.get_full_name', verbose_name=_('Writer'))
    quote = SafeColumn()
    topic = tables.Column(accessor='topic.title')
    quoted_by = tables.Column(accessor='quoted_by.get_full_name', verbose_name=_('Said by'))
    meter = ImageColumn(accessor='meter.image_small_text', verbose_name=_('Meter'))
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
    name = tables.Column(accessor='get_full_name', verbose_name=_('Name'))
    categories = tables.Column()
    status = StatusColumn()
    created = DateColumn()

    class Meta:
        model = People
        fields = ('created_by', 'image', 'name', 'categories', 'status', 'created')


class MyPeopleTable(PeopleTable):

    class Meta:
        exclude = ('created_by', )
