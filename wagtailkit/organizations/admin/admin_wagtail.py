from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect

from wagtail.contrib.modeladmin.views import CreateView
from wagtail.contrib.modeladmin.helpers import PermissionHelper
from wagtail.admin import messages
from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel,
    TabbedInterface, ObjectList)
from wagtail.documents.edit_handlers import DocumentChooserPanel

from wagtailkit.admin.admin import ModelAdmin
from wagtailkit.organizations.models import Department, Position


class DepartmentModelAdmin(ModelAdmin):
    model = Department
    list_per_page = 20
    menu_icon = ' icon-fa-sitemap'
    search_fields = ['name']
    list_filter = ['level']
    list_display = ['department_name', 'manager','parent']

    panels = [
        MultiFieldPanel([
            FieldPanel('parent'),
            FieldPanel('code'),
            FieldPanel('name'),
        ]),
    ]

    def department_name(self, obj):
        return "{} {}".format('---' * obj.level, obj.name)

    def manager(self, obj):
        return obj.get_manager_position()

    def co_manager(self, obj):
        return obj.get_co_manager_position()

    def get_queryset(self, request):
        return self.model.objects.all()

    def get_ordering(self, request):
        mptt_opts = self.model._mptt_meta
        return self.ordering or (mptt_opts.tree_id_attr, mptt_opts.left_attr)


class PositionModelAdmin(ModelAdmin):
    model = Position
    menu_icon = ' icon-fa-podcast'
    list_per_page = 20
    search_fields = ['name', 'department__name']
    list_filter = ['department__level']
    list_display = ['position_name', 'parent', 'is_manager', 'is_active']

    basic_panels = [
        MultiFieldPanel([
            FieldPanel('parent'),
            FieldPanel('name'),
            FieldPanel('department'),
            FieldPanel('is_manager'),
            FieldPanel('is_co_manager'),
            FieldPanel('is_active'),
            FieldPanel('employee_required'),
            DocumentChooserPanel('attachment'),
        ]),
    ]

    edit_handler = TabbedInterface([
        ObjectList(basic_panels, heading=_('Basic Information'))
    ])

    def position_name(self, obj):
        return "{} {}".format('---' * obj.level, obj.name)

    def get_ordering(self, request):
        mptt_opts = self.model._mptt_meta
        return self.ordering or (mptt_opts.tree_id_attr, mptt_opts.left_attr)