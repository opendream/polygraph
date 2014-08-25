import threading
from django.utils import translation
from django.conf import settings

evil_threadlocals = threading.local()

def get_request():
    try:
        return evil_threadlocals.request
    except AttributeError:
        return None

class EvilMiddleware(object):
    def process_request(self, request):
        evil_threadlocals.request = request


class ForceDefaultLanguageMiddleware(object):
    """
    Ignore Accept-Language HTTP headers
    
    This will force the I18N machinery to always choose settings.LANGUAGE_CODE
    as the default initial language, unless another one is set via sessions or cookies
    
    Should be installed *before* any middleware that checks request.META['HTTP_ACCEPT_LANGUAGE'],
    namely django.middleware.locale.LocaleMiddleware
    """
    def process_request(self, request):

        translation.activate(settings.LANGUAGE_CODE)

        if request.META.has_key('HTTP_ACCEPT_LANGUAGE'):
            del request.META['HTTP_ACCEPT_LANGUAGE']