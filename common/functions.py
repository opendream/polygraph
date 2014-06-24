from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _


from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
from django.utils.text import normalize_newlines
from common.constants import STATUS_PUBLISHED, STATUS_PENDING

register = template.Library()


def remove_newlines(text):
    """
    Removes all newline characters from a block of text.
    """
    # First normalize the newlines using Django's nifty utility
    normalized_text = normalize_newlines(text)
    # Then simply remove the newlines like so.
    return mark_safe(normalized_text.replace('\n', ' '))

def process_status(user, status, default=False):

    if default:
        return STATUS_PUBLISHED if user.is_staff else STATUS_PENDING

    status = int(status)
    if not user.is_staff and status == STATUS_PUBLISHED:
        status = STATUS_PENDING

    return status



def people_render_reference(people, display_edit_link=True, field_name='quoted_by'):

    html = '<span class="reference-span">%s</span>' % people.get_full_name()

    if people.image:
        html = '<img class="reference-span" src="%s" /> %s' % (people.image.thumbnail_100x100().url, html)

    if display_edit_link:
        html = '%s <a class="reference-span autocomplete-add-another" id="edit_id_%s" href="%s?_popup=1">%s</a>' % (html, field_name, reverse('people_edit', args=[people.id]), _('edit'))

    html = '<span class="people-reference-wrapper reference-wrapper">%s</span>' % html

    return html


def topic_render_reference(topic, display_edit_link=True, field_name='topic'):

    html = '<span class="reference-span">%s</span>' % topic.title

    used_to = [statement.quoted_by.get_short_name() for statement in topic.statement_set.order_by('-created')[0:3]]
    used_to = ', '.join(used_to)


    html = '%s<span class="reference-span">-- %s %s</span>' % (html, _('by'), used_to)

    if display_edit_link:
        html = '%s <a class="reference-span add-another-inline" id="edit_id_%s" href="%s?_inline=1" target="topic_inline">%s</a>' % (html, field_name, reverse('topic_edit', args=[topic.id]), _('edit'))

    html = '<span class="topic-reference-wrapper reference-wrapper">%s</span>' % html

    return html


def image_render(image, size):

    thumbnail = False
    if image:
        try:
            thumbnail = getattr(image, 'thumbnail_tag_%s' % size)()
        except:
            pass

    if not thumbnail:
        width, height = size.split('x')
        thumbnail = '<img src="%s" width="%s" height="%s" alt="no-image" />' % (settings.DEFAULT_IMAGE, width, height)

    return thumbnail

def meter_render_reference(meter, display_edit_link=False, field_name='meter'):

    html = '<div class="media-body"><span class="media-heading">%s</span></div>' % meter.title


    html = '<span class="pull-left image-wrapper">%s</span> %s' % (image_render(meter.image_small, '36x44'), html)

    html = '<div class="item-inner">%s</div>' % html

    return html

def statement_render_reference(statement, display_edit_link=True, field_name='relate_statements'):

    html = '<span class="reference-span">%s</span>' % remove_newlines(strip_tags(statement.quote))

    if display_edit_link:
        html = '%s <a class="reference-span autocomplete-add-another" id="edit_id_%s" href="%s?_popup=1">%s</a>' % (html, field_name, reverse('statement_edit', args=[statement.id]), _('edit'))

    html = '<span class="statement-reference-wrapper reference-wrapper">%s</span>' % html

    return html