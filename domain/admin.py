from django.contrib import admin

from domain.models import PeopleCategory, People, Topic, TopicRevision, Meter, Statement

class TopicRevisionInline(admin.TabularInline):
    model = TopicRevision


class TopicAdmin(admin.ModelAdmin):
    inlines = [ TopicRevisionInline, ]

class MeterAdmin(admin.ModelAdmin):
    list_display = ('image_small', 'title')

admin.site.register(PeopleCategory)
admin.site.register(People)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Meter, MeterAdmin)
admin.site.register(Statement)