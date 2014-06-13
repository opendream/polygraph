from django.conf import settings


def helper(request):
    context = {
        'request_popup': bool(request.GET.get('_popup')),
        'request_inline': bool(request.GET.get('_inline')),
    }

    return context