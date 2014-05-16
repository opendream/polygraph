from django.contrib import admin

from domain.models import Staff


class StaffAdmin(admin.ModelAdmin):
    pass

admin.site.register(Staff, StaffAdmin)
