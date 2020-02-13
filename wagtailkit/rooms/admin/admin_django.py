from django.contrib import admin
from wagtailkit.rooms.models import Room

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    search_fields = ['name', 'code']
    list_display = ['name', 'code', 'building']