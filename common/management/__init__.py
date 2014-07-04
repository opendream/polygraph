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

    if not os.path.exists('%sdefault' % full_dir):
        shutil.copytree('.%s' % os.path.join(settings.STATIC_URL, 'images/default'), '%sdefault' % full_dir)

    Meter.objects.get_or_create(permalink='unverifiable', defaults={
        'title': 'Unverifiable',
        'description': 'This is unverifiable description. Please, edit me on the admin site.',
        'point': 0,
        'image_large_text': '%sdefault_meters/status-unverifiable---large-text.png' % settings.FILES_WIDGET_TEMP_DIR,
        'image_medium_text': '%sdefault_meters/status-unverifiable---medium-text.png' % settings.FILES_WIDGET_TEMP_DIR,
        'image_small_text': '%sdefault_meters/status-unverifiable---small-text.png' % settings.FILES_WIDGET_TEMP_DIR,
        'image_small': '%sdefault_meters/status-unverifiable---small.png' % settings.FILES_WIDGET_TEMP_DIR,

        'order': 3
    })
    Meter.objects.get_or_create(permalink='half-truth', defaults={
        'title': 'Half True',
        'description': 'This is half truth description. Please, edit me on the admin site.',
        'point': -1,
        'image_large_text': '%sdefault_meters/status-half-truth---large-text.png' % settings.FILES_WIDGET_TEMP_DIR,
        'image_medium_text': '%sdefault_meters/status-half-truth---medium-text.png' % settings.FILES_WIDGET_TEMP_DIR,
        'image_small_text': '%sdefault_meters/status-half-truth---small-text.png' % settings.FILES_WIDGET_TEMP_DIR,
        'image_small': '%sdefault_meters/status-half-truth---small.png' % settings.FILES_WIDGET_TEMP_DIR,
        'order': 2
    })
    Meter.objects.get_or_create(permalink='lie', defaults={
        'title': 'Lie',
        'description': 'This is lie description. Please, edit me on the admin site.',
        'point': -2,
        'image_large_text': '%sdefault_meters/status-lie---large-text.png' % settings.FILES_WIDGET_TEMP_DIR,
        'image_medium_text': '%sdefault_meters/status-lie---medium-text.png' % settings.FILES_WIDGET_TEMP_DIR,
        'image_small_text': '%sdefault_meters/status-lie---small-text.png' % settings.FILES_WIDGET_TEMP_DIR,
        'image_small': '%sdefault_meters/status-lie---small.png' % settings.FILES_WIDGET_TEMP_DIR,
        'order': 1
    })
    Meter.objects.get_or_create(permalink='truth', defaults={
        'title': 'Truth',
        'description': 'This is truth description. Please, edit me on the admin site.',
        'point': 2,
        'image_large_text': '%sdefault_meters/status-truth---large-text.png' % settings.FILES_WIDGET_TEMP_DIR,
        'image_medium_text': '%sdefault_meters/status-truth---medium-text.png' % settings.FILES_WIDGET_TEMP_DIR,
        'image_small_text': '%sdefault_meters/status-truth---small-text.png' % settings.FILES_WIDGET_TEMP_DIR,
        'image_small': '%sdefault_meters/status-truth---small.png' % settings.FILES_WIDGET_TEMP_DIR,
        'order':0
    })

    PeopleCategory.objects.get_or_create(permalink='politician', defaults={
        'title': 'Politician',
        'description': 'This is politician description. Please, edit me on the admin site.'
    })

    PeopleCategory.objects.get_or_create(permalink = 'government', defaults={
        'title': 'Government',
        'description': 'This is government description. Please, edit me on the admin site.',
    })

    PeopleCategory.objects.get_or_create(permalink = 'public-figure', defaults={
        'title': 'Public Figure',
        'description': 'This is public figure description. Please, edit me on the admin site.',
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

