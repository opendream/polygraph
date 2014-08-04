from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _
from django.db.models.query import QuerySet


from django import template
from django.utils.safestring import mark_safe
from django.utils.text import normalize_newlines
from django.template.loader_tags import BlockNode, ExtendsNode
from django.template import loader, Context

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

def get_success_message(inst, is_new=False):

    inst_name = inst.inst_name.lower()
    key = inst.permalink if hasattr(inst, 'permalink') else inst.id

    if is_new:
        return  _('New %s has been created. View this %s <a href="%s">here</a>.') % (
            _(inst_name),
            _(inst_name),
            reverse('%s_detail' % inst_name, args=[key])
        )
    else:
        return _('Your %s settings has been updated. View this %s <a href="%s">here</a>.') % (
            _(inst_name),
            _(inst_name),
            reverse('%s_detail' % inst_name, args=[key])
        )


def people_render_reference(people, display_edit_link=True, field_name='quoted_by'):

    html = '<span class="reference-span">%s</span>' % people.get_full_name()

    if people.image:
        html = '<img class="reference-span" src="%s" /> %s' % (people.image.thumbnail_100x100().url, html)

    if display_edit_link:
        html = '%s <a class="reference-span autocomplete-add-another" id="edit_id_%s" href="%s?_popup=1"><span class="glyphicon glyphicon-edit"></span> %s</a>' % (html, field_name, reverse('people_edit', args=[people.id]), _('edit'))

    html = '<span class="people-reference-wrapper reference-wrapper">%s</span>' % html

    return html


def topic_render_reference(topic, display_edit_link=True, field_name='topic'):

    from domain.models import Statement

    html = '<span class="reference-span">%s</span>' % topic.title
    
    query = topic.statement_set.order_by('-created').query
    query.group_by = ['quoted_by_id']
    used_to = QuerySet(query=query, model=Statement)

    used_to = [statement.quoted_by.get_short_name() for statement in used_to[0:3]]

    if used_to:
        used_to = ', '.join(used_to)
        html = '%s<span class="reference-span">-- %s %s</span>' % (html, _('by'), used_to)

    if display_edit_link:
        html = '%s <a class="reference-span add-another-inline" id="edit_id_%s" href="%s?_inline=1" target="topic_inline"><span class="glyphicon glyphicon-edit"></span> %s</a>' % (html, field_name, reverse('topic_edit', args=[topic.id]), _('edit'))

    html = '<span class="topic-reference-wrapper reference-wrapper">%s</span>' % html

    return html


def image_render(image, size, alt=''):

    thumbnail = False
    if image:
        try:
            thumbnail = getattr(image, 'thumbnail_tag_%s' % size)()
            if 'alt=' not in thumbnail:
                thumbnail = thumbnail.replace('/>', 'alt="%s" />' % alt)

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
        html = '%s <a class="reference-span autocomplete-add-another" id="edit_id_%s" href="%s?_popup=1"><span class="glyphicon glyphicon-edit"></span> %s</a>' % (html, field_name, reverse('statement_edit', args=[statement.id]), _('edit'))

    html = '<span class="statement-reference-wrapper reference-wrapper">%s</span>' % html

    return html


# Render specific blocks from templates

def get_template(template):
    if isinstance(template, (tuple, list)):
        return loader.select_template(template)
    return loader.get_template(template)

class BlockNotFound(Exception):
    pass

def render_template_block(template, block, context):
    """
    Renders a single block from a template. This template should have previously been rendered.
    """
    return render_template_block_nodelist(template.nodelist, block, context)

def render_template_block_nodelist(nodelist, block, context):
    for node in nodelist:
        if isinstance(node, BlockNode) and node.name == block:
            return node.render(context)
        for key in ('nodelist', 'nodelist_true', 'nodelist_false'):
            if hasattr(node, key):
                try:
                    return render_template_block_nodelist(getattr(node, key), block, context)
                except:
                    pass
    for node in nodelist:
        if isinstance(node, ExtendsNode):
            try:
                return render_template_block(node.get_parent(context), block, context)
            except BlockNotFound:
                pass
    raise BlockNotFound

def render_block_to_string(template_name, block, dictionary=None, context_instance=None):
    """
    Loads the given template_name and renders the given block with the given dictionary as
    context. Returns a string.
    """
    dictionary = dictionary or {}
    t = get_template(template_name)
    if context_instance:
        context_instance.update(dictionary)
    else:
        context_instance = Context(dictionary)
    t.render(context_instance)
    return render_template_block(t, block, context_instance)
