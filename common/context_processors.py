import os
from django.conf import settings
from common.constants import STATUS_PENDING, STATUS_PUBLISHED, STATUS_DRAFT
from common.functions import render_block_to_string


def helper(request):


    static_page_list = []
    for page in os.listdir(settings.PAGE_ROOT):

        if '.html' in page:
            static_page_list.append({
                'url_name': page.replace('.html', ''),
                'title': render_block_to_string(page, 'title')
            })

    context = {
        'request_popup': bool(request.GET.get('_popup') or request.POST.get('_popup')),
        'request_inline': bool(request.GET.get('_inline') or request.POST.get('_inline')),
        'request_pagination': request.GET.get('page'),
        'static_page_list': static_page_list,
        'SITE_LOGO_URL': settings.SITE_LOGO_URL,
        'SITE_NAME': settings.SITE_NAME,
        'STATUS_PUBLISHED': STATUS_PUBLISHED,
        'STATUS_PENDING': STATUS_PENDING,
        'STATUS_DRAFT': STATUS_DRAFT
    }

    return context