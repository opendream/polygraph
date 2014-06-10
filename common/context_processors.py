from django.conf import settings


def helper(request):
    context = {
        'request_popup': bool(request.GET.get('_popup')),
    }

    return context