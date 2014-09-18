from uuid import uuid1
from django.core import validators
from django.core.cache import cache
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from ckeditor.fields import RichTextField

import re
from common.constants import NO_IP
from common.middleware import get_request
import files_widget



class CommonTrashManager(models.Manager):
    def filter_without_trash(self, *args, **kwargs):
        if not kwargs.get('is_deleted'):
            return super(CommonTrashManager, self).filter(*args, **kwargs).exclude(is_deleted=True)
        else:
            return super(CommonTrashManager, self).filter(*args, **kwargs)

    def exclude(self, *args, **kwargs):
        if not kwargs.get('is_deleted'):
            return super(CommonTrashManager, self).exclude(*args, **kwargs).exclude(is_deleted=True)

    def filter(self, *args, **kwargs):
        return self.filter_without_trash(*args, **kwargs)

    def all(self, *args, **kwargs):
        return self.filter(*args, **kwargs)

    def get_without_trash(self, *args, **kwargs):
        if not kwargs.get('is_deleted'):
            kwargs['is_deleted'] = False
        return super(CommonTrashManager, self).get(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.get_without_trash(*args, **kwargs)

    def annotate(self, *args, **kwargs):
        return super(CommonTrashManager, self).exclude(is_deleted=True).annotate(*args, **kwargs)


class CommonModel(models.Model):

    @property
    def inst_name(self):
        return self.__class__.__name__

    class Meta:
        abstract = True

class CommonTrashModel(models.Model):
    is_deleted  = models.BooleanField(default=False)
    objects = CommonTrashManager()

    def save(self, *args, **kwargs):

        cache.clear()
        super(CommonTrashModel, self).save(*args, **kwargs)

    def trash(self, *args, **kwargs):

        self.is_deleted = True

        if hasattr(self, 'permalink'):
            self.permalink = 'deleted_%s_%s' % (str(uuid1())[0: 10].replace('-', ''), self.permalink)

        self.save()
        return self

    def delete(self, *args, **kwargs):
        return self.trash(self, *args, **kwargs)

    @property
    def total_views(self):

        content_type = ContentType.objects.get_for_model(self)

        try:
            return StatisitcTotal.objects.get(content_type=content_type, object_id=self.id).value
        except StatisitcTotal.DoesNotExist:
            return 0

    class Meta:
        abstract = True


class AbstractPeopleField(models.Model):

    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)

    occupation = models.CharField(max_length=255, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    homepage_url = models.CharField(max_length=255, null=True, blank=True)

    image = files_widget.ImageField(null=True, blank=True)


    class Meta:
        abstract = True



    def get_full_name(self):

        try:
            full_name = '%s %s' % (self.first_name, self.last_name)
            return full_name.strip()
        except:
            return ''

    def get_short_name(self):

        try:
            if self.first_name.strip() and self.last_name.strip():
                return '%s.%s' % (self.first_name.strip(), self.last_name.strip()[0])

            elif self.first_name.strip():
                return self.first_name.strip()

            elif self.last_name.strip():
                return self.last_name.strip()

            return ''
        except:
            return ''

    def __unicode__(self):
        return self.get_full_name()


class AbstractPermalink(CommonModel):

    class Meta:
        abstract = True

    permalink = models.CharField(max_length=255, unique=True,
        help_text=_('Required unique 30 characters or fewer. Letters, numbers and ./@/+/-/_ characters'),
        validators=[
            validators.RegexValidator(re.compile('^[\w.+-]+$'), _('Enter a valid permalink.'), 'invalid')
        ])

    def __unicode__(self):
        return self.permalink


class StatisitcTotal(models.Model):

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    value = models.PositiveIntegerField()


class StatisitcAccess(models.Model):

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    created = models.DateTimeField(auto_now_add=True)
    ip_address = models.IPAddressField(default=NO_IP)

    def save(self, *args, **kwargs):

        request = get_request()
        try:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                self.ip_address = x_forwarded_for.split(',')[0]
            else:
                self.ip_address = request.META.get('REMOTE_ADDR')
        except:
            self.ip_address = NO_IP

        if not self.ip_address:
            self.ip_address = NO_IP

        try:
            total = StatisitcTotal.objects.get(content_type=self.content_type, object_id=self.object_id)
            total.value = total.value + 1
            total.save()

        except StatisitcTotal.DoesNotExist:
            StatisitcTotal.objects.create(content_type=self.content_type, object_id=self.object_id, value=1)

        super(StatisitcAccess, self).save(*args, **kwargs)


class Variable(models.Model):

    name = models.CharField(max_length=60, unique=True)
    value = models.TextField(null=True, blank=True)


