from django.utils import translation, html
from django.contrib import admin

from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.admin.edit_handlers import (
    ObjectList, TabbedInterface, FieldPanel, RichTextFieldPanel,
    MultiFieldPanel, InlinePanel, FieldRowPanel)
from wagtail.contrib.modeladmin.options import ModelAdmin

from wagtailkit.rooms.models import Room

_ = translation.gettext_lazy

LIST_PER_PAGE = 20

class RoomModelAdmin(ModelAdmin):
    model = Room
    menu_icon = 'fa-columns'
    menu_label = _('Rooms')
    list_per_page = LIST_PER_PAGE
    list_display = ['code', 'name', 'building', 'capacity']
    edit_handler = ObjectList([
        MultiFieldPanel([
            FieldPanel('code'),
            FieldPanel('name'),
            FieldPanel('building'),
            FieldPanel('capacity')
        ])
    ])