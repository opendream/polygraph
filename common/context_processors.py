from django.conf import settings
from common.constants import STATUS_PENDING, STATUS_PUBLISHED, STATUS_DRAFT


def helper(request):
    context = {
        'request_popup': bool(request.GET.get('_popup') or request.POST.get('_popup')),
        'request_inline': bool(request.GET.get('_inline') or request.POST.get('_inline')),
        'request_pagination': request.GET.get('page'),
        'STATUS_PUBLISHED': STATUS_PUBLISHED,
        'STATUS_PENDING': STATUS_PENDING,
        'STATUS_DRAFT': STATUS_DRAFT
    }

    return context