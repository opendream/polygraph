from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _




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
        html = '%s <a class="reference-span add-another-inline" id="edit_id_%s" href="%s?_popup=1&_inline=1" target="topic_inline">%s</a>' % (html, field_name, reverse('topic_edit', args=[topic.id]), _('edit'))

    html = '<span class="topic-reference-wrapper reference-wrapper">%s</span>' % html

    return html