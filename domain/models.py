import jsonfrom datetime import timedeltafrom django.conf import settingsfrom django.contrib.auth import get_user_modelfrom django.db import modelsfrom django.utils import timezonefrom django.utils.translation import ugettext_lazy as _from ckeditor.fields import RichTextFieldimport taggingfrom common.functions import meter_render_referencefrom common.models import CommonTrashModel, AbstractPermalink, AbstractPeopleField, CommonModelfrom common.constants import STATUS_DRAFT, STATUS_PENDING, STATUS_PUBLISHEDfrom collections import namedtupleimport files_widgetfrom tagging_autocomplete_tagit.models import TagAutocompleteTagItFieldclass PeopleCategory(AbstractPermalink):    title = models.CharField(max_length=255)    description = RichTextField(null=True, blank=True)    def __unicode__(self):        return self.titleclass People(CommonTrashModel, AbstractPeopleField, AbstractPermalink):    categories = models.ManyToManyField(PeopleCategory)    created_by = models.ForeignKey(get_user_model())    status = models.IntegerField(default=STATUS_PUBLISHED)    created = models.DateTimeField(auto_now_add=True)    changed = models.DateTimeField(auto_now=True)class Topic(CommonModel, CommonTrashModel):    # created_by, title, description ,created ,changed    def __init__(self, *args, **kwargs):        super(Topic, self).__init__(*args, **kwargs)        # Prepare field on the fly in memory before database saved        self.revision_fields = {}        self.revision_fields['created_by'] = kwargs.get('created_by')        self.revision_fields['title'] = kwargs.get('title')        self.revision_fields['description'] = kwargs.get('description')        self.revision_fields['created'] = kwargs.get('created')        self.revision_fields['changed'] = kwargs.get('changed')        # convert dict to object for similar model object        RevisionStruct = namedtuple('RevisionStruct', ' '.join(self.revision_fields.keys()))        revision_struct_fields = RevisionStruct(**self.revision_fields)        self.latest_revision = revision_struct_fields        self.oldest_revision = revision_struct_fields        topic_revision_list = self.topicrevision_set.order_by('-id')        try:            self.latest_revision = topic_revision_list[0]            self.oldest_revision = topic_revision_list[topic_revision_list.count()-1]        except (AssertionError, IndexError):            pass        # Assign attributes from revisions        self._created_by = self.latest_revision.created_by        self._title = self.latest_revision.title        self._description = self.latest_revision.description        self._created = self.oldest_revision.created        self._changed = self.latest_revision.created        for field, value in kwargs.items():            setattr(self, '_%s' % field, value)    @property    def created_by(self):        return self._created_by    @property    def title(self):        return self._title    @property    def description(self):        return self._description    @property    def created(self):        return self._created    @property    def changed(self):        return self._changed    @created_by.setter    def created_by(self, value):        self._created_by = value    @title.setter    def title(self, value):        self._title = value    @description.setter    def description(self, value):        self._description = value    @created.setter    def created(self, value):        self._created = value    @changed.setter    def changed(self, value):        self._changed = value    def __unicode__(self):        return self.title    def save(self, without_revision=False, *args, **kwargs):        if not self._changed:            self._changed = timezone.now()        if not without_revision or not hasattr(self.latest_revision, 'id'):            self.latest_revision = TopicRevision.objects.create(                created_by = self._created_by,                title = self._title,                description = self._description,                created = self._changed            )        else:            self.latest_revision.created_by = self._created_by            self.latest_revision.title = self._title            self.latest_revision.description = self._description            self.latest_revision.created = self._changed            self.latest_revision.save()        if self._created:            self.oldest_revision.created = self._created            self.oldest_revision.save()        super(Topic, self).save(*args, **kwargs)        self.latest_revision.origin = self        self.latest_revision.save()    def delete(self, *args, **kwargs):        super(Topic, self).delete(*args, **kwargs)        TopicRevision.objects.filter(origin__id=self.id).delete()class TopicRevision(CommonTrashModel):    origin = models.ForeignKey(Topic, null=True)    created_by = models.ForeignKey(get_user_model())    title = models.CharField(max_length=255)    description = RichTextField(null=True, blank=True)    created = models.DateTimeField()class Meter(CommonTrashModel, AbstractPermalink):    title = models.CharField(max_length=255)    description = RichTextField(null=True, blank=True)    point = models.IntegerField(default=0)    order = models.IntegerField(default=0)    image_large_text = files_widget.ImageField(null=True, blank=True)    image_medium_text = files_widget.ImageField(null=True, blank=True)    image_small_text = files_widget.ImageField(null=True, blank=True)    image_small = files_widget.ImageField(null=True, blank=True)    def __unicode__(self):        return meter_render_reference(self)class Statement(CommonTrashModel, AbstractPermalink):    quoted_by = models.ForeignKey(People, related_name='quoted_by')    created_by = models.ForeignKey(get_user_model(), related_name='created_by')    published_by = models.ForeignKey(get_user_model(), related_name='published_by', null=True, blank=True)    relate_statements = models.ManyToManyField('self', null=True, blank=True, related_name='relate_statements')    relate_peoples = models.ManyToManyField(People, null=True, blank=True, related_name='relate_peoples')    quote = RichTextField()    _references = models.TextField(null=True, blank=True)    topic = models.ForeignKey(Topic, null=True, blank=True, on_delete=models.SET_NULL)    tags = TagAutocompleteTagItField(max_tags=False, null=True, blank=True)    meter = models.ForeignKey(Meter, null=True, blank=True)    source = models.CharField(max_length=255, null=True, blank=True)    status = models.IntegerField(default=STATUS_PENDING)    created = models.DateTimeField(null=True, blank=True)    changed = models.DateTimeField(null=True, blank=True)    published = models.DateTimeField(null=True, blank=True)    @property    def references(self):        self._references = self._references or '[]'        return json.loads(self._references)    @references.setter    def references(self, value):        value = value or []        self._references = json.dumps(value)    def __unicode__(self):        return self.quote    @property    def uptodate_status(self):        outdate = timezone.now() - timedelta(days=settings.UPTODATE_DAYS)        # Don't refactor this if case it's short hand for check None        if self.status not in [STATUS_DRAFT, STATUS_PENDING] and ((self.created and self.created >= outdate) or (self.changed and self.changed >= outdate)):            if self.created and not self.changed:                return {'code': 'new', 'text': _('New')}            elif self.created and self.changed:                return {'code': 'updated', 'text': _('Updated')}        return False    def save(self, *args, **kwargs):        try:            before = Statement.objects.get(id=self.id)        except:            before = self        if not before.created and self.status != STATUS_DRAFT:            self.created = timezone.now()        if before.id and not before.changed and self.status not in [STATUS_DRAFT, STATUS_PENDING] and before.status not in [STATUS_DRAFT, STATUS_PENDING]:            self.changed = timezone.now()        super(Statement, self).save(*args, **kwargs)tagging.register(Statement, tag_descriptor_attr='tag_set')