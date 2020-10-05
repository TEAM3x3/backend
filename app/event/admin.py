from django.contrib import admin

from event.models import Event, MainEvent, MainEventType


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'image', 'square_image']


@admin.register(MainEvent)
class MainEventAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'image']


@admin.register(MainEventType)
class MainEventType(admin.ModelAdmin):
    list_display = ['id', 'name', 'event']
