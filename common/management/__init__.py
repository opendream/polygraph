from django.contrib.auth import models as auth_models
from django.contrib.auth.management import create_superuser
from django.db.models.signals import post_syncdb
from account.models import Staff

from domain.models import Meter, PeopleCategory
from common import models as common_models

import sys


post_syncdb.disconnect(
    create_superuser,
    sender=auth_models,
    dispatch_uid='django.contrib.auth.management.create_superuser'
)



def create_common(app, created_models, verbosity, **kwargs):


    if 'test' in sys.argv:
        return


    Meter.objects.get_or_create( permalink='true', defaults={
        'title': 'True',
        'description': 'This is true description. Please, edit me on the admin site.',
        'point': 2,

        'order':0
    })
    Meter.objects.get_or_create(permalink='false', defaults={
        'title': 'False',
        'description': 'This is unprovable description. Please, edit me on the admin site.',
        'point': -2,

        'order': 1
    })
    Meter.objects.get_or_create(permalink='tricky', defaults={
        'title': 'Tricky',
        'description': 'This is tricky description. Please, edit me on the admin site.',
        'point': -1,

        'order': 2
    })
    Meter.objects.get_or_create(permalink='unprovable', defaults={
        'title': 'Unprovable',
        'description': 'This is unprovable description. Please, edit me on the admin site.',
        'point': 0,

        'order': 3
    })


    PeopleCategory.objects.get_or_create(permalink='politician', defaults={
        'title': 'Politician',
        'description': 'This is politician description. Please, edit me on the admin site.'
    })

    PeopleCategory.objects.get_or_create(permalink = 'military', defaults={
        'title': 'Military',
        'description': 'This is military description. Please, edit me on the admin site.',
    })


    try:
        Staff.objects.get(username='admin')
    except Staff.DoesNotExist:

        Staff.objects.create_superuser(
            username = 'admin',
            email = 'admin@polygraph.ex',
            first_name = 'Admin',
            last_name = 'Polygraph',
            password = 'password'
        )


post_syncdb.connect(
    create_common,
    sender=common_models,
    dispatch_uid='common.management'
)