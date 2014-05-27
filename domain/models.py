from django.core import validatorsfrom django.db import modelsfrom django.utils.translation import ugettext_lazy as _from ckeditor.fields import RichTextFieldimport reclass AbstractPeopleField(models.Model):    first_name = models.CharField(_('first name'), max_length=30, null=True, blank=True)    last_name = models.CharField(_('last name'), max_length=30, null=True, blank=True)    occupation = models.CharField(max_length=255, null=True, blank=True)    description = RichTextField(null=True, blank=True)    homepage_url = models.CharField(max_length=255, null=True, blank=True)    class Meta:        abstract = True    def get_full_name(self):        """        Returns the first_name plus the last_name, with a space in between.        """        full_name = '%s %s' % (self.first_name, self.last_name)        return full_name.strip()    def get_short_name(self):        "Returns the short name for the user."        if self.first_name.strip() and self.last_name.strip():            return '%s.%s' % (self.first_name.strip(), self.last_name.strip()[0])        elif self.first_name.strip():            return self.first_name.strip()        elif self.last_name.strip():            return self.last_name.strip()        return '';class People(AbstractPeopleField):    permalink = models.CharField(_('permalink'), max_length=30, unique=True,        help_text=_('Required unique 30 characters or fewer. Letters, numbers and '                    './+/-/_ characters'),        validators=[            validators.RegexValidator(re.compile('^[\w.+-]+$'), _('Enter a valid permalink.'), 'invalid')        ])    def __unicode__(self):        return self.permalink    @property    def inst_name(self):        return _(self.__class__.__name__)