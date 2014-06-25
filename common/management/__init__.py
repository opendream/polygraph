import distutils
from django.conf import settings
from django.contrib.auth import models as auth_models
from django.contrib.auth.management import create_superuser
from django.db.models.signals import post_syncdb
import shutil
from account.models import Staff

from domain.models import Meter, PeopleCategory
from common import models as common_models

import sys, os


post_syncdb.disconnect(
    create_superuser,
    sender=auth_models,
    dispatch_uid='django.contrib.auth.management.create_superuser'
)



def create_common(app, created_models, verbosity, **kwargs):


    if 'test' in sys.argv:
        return

    full_dir = os.path.join(settings.MEDIA_ROOT, settings.FILES_WIDGET_TEMP_DIR)
    if not os.path.exists(full_dir):
        os.makedirs(full_dir)

    if not os.path.exists('%sdefault_meters' % full_dir):
        shutil.copytree('.%s' % os.path.join(settings.STATIC_URL, 'images/default_meters'), '%sdefault_meters' % full_dir)

    Meter.objects.get_or_create(permalink='unprovable', defaults={
        'title': 'Unprovable',
        'description': 'This is unprovable description. Please, edit me on the admin site.',
        'point': 0,
        'image_small': '%sdefault_meters/image_small_unprovable.png' % settings.FILES_WIDGET_TEMP_DIR,

        'order': 3
    })
    Meter.objects.get_or_create(permalink='tricky', defaults={
        'title': 'Tricky',
        'description': 'This is tricky description. Please, edit me on the admin site.',
        'point': -1,
        'image_small': '%sdefault_meters/image_small_tricky.png' % settings.FILES_WIDGET_TEMP_DIR,

        'order': 2
    })
    Meter.objects.get_or_create(permalink='false', defaults={
        'title': 'False',
        'description': 'This is unprovable description. Please, edit me on the admin site.',
        'point': -2,
        'image_small': '%sdefault_meters/image_small_false.png' % settings.FILES_WIDGET_TEMP_DIR,

        'order': 1
    })
    Meter.objects.get_or_create( permalink='true', defaults={
        'title': 'True',
        'description': 'This is true description. Please, edit me on the admin site.',
        'point': 2,
        'image_small': '%sdefault_meters/image_small_true.png' % settings.FILES_WIDGET_TEMP_DIR,

        'order':0
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

    try:
        Staff.objects.get(username='writer')
    except Staff.DoesNotExist:

        Staff.objects.create_user(
            username = 'writer',
            email = 'writer@polygraph.ex',
            first_name = 'Wriet',
            last_name = 'Polygraph',
            password = 'password'
        )


post_syncdb.connect(
    create_common,
    sender=common_models,
    dispatch_uid='common.management'
)