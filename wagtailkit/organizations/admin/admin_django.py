from django.contrib import admin
from django.utils import translation, timezone
from mptt.admin import MPTTModelAdmin

from wagtailkit.organizations.models import Department, Position

_ = translation.gettext_lazy


@admin.register(Department)
class DepartmentAdmin(MPTTModelAdmin):
    show_in_index = True
    search_fields = ['name']
    list_display = ['name', 'code', 'level']


@admin.register(Position)
class PositionAdmin(MPTTModelAdmin):
    show_in_index = True
    search_fields = ['department__name']
    list_select_related = ['department']
    list_display = ['name', 'level', 'department', 'is_manager', 'is_co_manager']