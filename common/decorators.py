from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import resolve
from common.models import StatisitcAccess

from functools import wraps


def statistic(view_func=None):

    def _decorator(request, *args, **kwargs):

        content_type = ''.join([c.title() for c in view_func.__name__.split('_')[0:-1]])

        content_type = ContentType.objects.get_by_natural_key(resolve(request.path).app_name, content_type.lower())
        content_type_id_key = request.resolver_match.kwargs.keys()[0]

        object_id = request.resolver_match.kwargs[content_type_id_key]

        if 'permalink' in content_type_id_key:
            object_id = content_type.model_class().objects.get(permalink=object_id).id


        StatisitcAccess.objects.create(content_type=content_type, object_id=object_id)
        response = view_func(request, *args, **kwargs)

        return response

    return wraps(view_func)(_decorator)
