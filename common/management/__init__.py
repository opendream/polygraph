from django.contrib.auth import models as auth_models
from django.contrib.auth.management import create_superuser
from django.db.models.signals import post_syncdb


post_syncdb.disconnect(
    create_superuser,
    sender=auth_models,
    dispatch_uid='django.contrib.auth.management.create_superuser'
)


