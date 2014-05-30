from django.contrib import admin

from domain.models import PeopleCategory, People, Topic, TopicRevision


class StaffAdmin(admin.ModelAdmin):
    pass

admin.site.register(PeopleCategory)
admin.site.register(People)
admin.site.register(Topic)
admin.site.register(TopicRevision)