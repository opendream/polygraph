from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _




def people_render_reference(people, display_edit_link=True, field_name='quoted_by'):

    html = '<span class="people-full-name">%s</span>' % people.get_full_name()

    if people.image:
        html = '<img src="%s" /> %s' % (people.image.thumbnail_100x100().url, html)

    if display_edit_link:
        html = '%s <a class="autocomplete-add-another" id="edit_id_%s" href="%s?_popup=1">%s</a>' % (html, field_name, reverse('people_edit', args=[people.id]), _('edit'))

    html = '<span class"people-reference-wrapper">%s</span>' % html

    return html