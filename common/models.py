from django.core import validators
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ckeditor.fields import RichTextField

import re
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


class CommonTrashModel(models.Model):
    is_deleted  = models.BooleanField(default=False)
    objects = CommonTrashManager()

    def trash(self, *args, **kwargs):
        self.is_deleted = True;
        self.save()
        return self

    def delete(self, *args, **kwargs):
        return self.trash(self, *args, **kwargs)

    class Meta:
        abstract = True


class AbstractPeopleField(models.Model):

    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)

    occupation = models.CharField(max_length=255, null=True, blank=True)
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


class AbstractPermalink(models.Model):

    class Meta:
        abstract = True

    permalink = models.CharField(max_length=30, unique=True,
        help_text=_('Required unique 30 characters or fewer. Letters, numbers and '
                    './+/-/_ characters'),
        validators=[
            validators.RegexValidator(re.compile('^[\w.+-]+$'), _('Enter a valid permalink.'), 'invalid')
        ])

    def __unicode__(self):
        return self.permalink

    @property
    def inst_name(self):
        return _(self.__class__.__name__)