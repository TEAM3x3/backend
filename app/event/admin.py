from django.contrib import admin

from event.models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


admin.site.register(Event, EventAdmin)
