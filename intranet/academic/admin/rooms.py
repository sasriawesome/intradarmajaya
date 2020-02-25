from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdminGroup

from wagtailkit.rooms.admin import (
    RoomModelAdmin
)

class RoomModelAdminGroup(ModelAdminGroup):
    menu_label = _('Rooms')
    menu_icon = 'fa-columns'
    items = [
        RoomModelAdmin
    ]