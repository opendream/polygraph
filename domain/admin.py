from django.contrib import admin
from common.functions import meter_render_reference

from domain.models import PeopleCategory, People, Topic, TopicRevision, Meter, Statement

class TopicRevisionInline(admin.TabularInline):
    model = TopicRevision


class TopicAdmin(admin.ModelAdmin):
    inlines = [ TopicRevisionInline, ]

class MeterAdmin(admin.ModelAdmin):

    list_display = ('rendered', )

    def rendered(self, obj):
        return meter_render_reference(obj)

    rendered.allow_tags = True

admin.site.register(PeopleCategory)
admin.site.register(People)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Meter, MeterAdmin)
admin.site.register(Statement)