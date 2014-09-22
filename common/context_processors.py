import os
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from common.constants import STATUS_PENDING, STATUS_PUBLISHED, STATUS_DRAFT
from common.functions import render_block_to_string
from common.models import Variable


def helper(request):


    static_page_list = []
    for page in os.listdir(settings.PAGE_ROOT):

        if '.html' in page:
            static_page_list.append({
                'url_name': page.replace('.html', ''),
                'title': render_block_to_string(page, 'title')
            })

    if request.user.is_staff:
        hilight_label, created = Variable.objects.get_or_create(name='highlight_label')
        hilight_label = hilight_label.value or _('Highlight')

    context = {
        'request_popup': bool(request.GET.get('_popup') or request.POST.get('_popup')),
        'request_inline': bool(request.GET.get('_inline') or request.POST.get('_inline')),
        'request_pagination': request.GET.get('page'),
        'static_page_list': static_page_list,
        'BASE_URL': request.build_absolute_uri('/')[0:-1],
        'SITE_LOGO_URL': settings.SITE_LOGO_URL,
        'SITE_NAME': settings.SITE_NAME,
        'SITE_FAVICON_URL': settings.SITE_FAVICON_URL,
        'STATUS_PUBLISHED': STATUS_PUBLISHED,
        'STATUS_PENDING': STATUS_PENDING,
        'STATUS_DRAFT': STATUS_DRAFT,
        'GOOGLE_ANALYTICS_KEY': settings.GOOGLE_ANALYTICS_KEY,
        'hilight_label': hilight_label
    }

    return context