from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.shortcuts import redirect, reverse

from wagtail.contrib.modeladmin.views import CreateView
from wagtail.contrib.modeladmin.helpers import PermissionHelper
from wagtail.admin.menu import MenuItem
from wagtail.admin import messages
from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel,
    TabbedInterface, ObjectList)
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.contrib.modeladmin.options import modeladmin_register, ModelAdminGroup
from wagtail.contrib.modeladmin.views import WMABaseView

from wagtailautocomplete.edit_handlers import AutocompletePanel
from wagtailkit.admin.admin import ModelAdmin
from wagtailkit.persons.admin import PersonModelAdmin
from wagtailkit.employees.models import PersonAsEmployee, Chair, Employee, Department


class PersonAsEmployeeModelAdmin(PersonModelAdmin):
    model = PersonAsEmployee


class EmployeeCreateView(CreateView):
    def get_instance(self):
        instance = super().get_instance()
        instance.creator = self.request.user
        return instance

    def form_valid(self, form):
        instance = form.save()
        messages.success(
            self.request, self.get_success_message(instance),
            buttons=self.get_success_message_buttons(instance)
        )
        return redirect(self.get_success_url())


class EmployeeDataPermissionHelper(PermissionHelper):
    pass


class EmployeeModelAdmin(ModelAdmin):
    model = Employee
    menu_label = _('Employee')
    menu_icon = ' icon-fa-drivers-license'
    search_fields = ['eid', 'person__firstname', 'person__lastname', 'department__name']
    list_filter = ['is_active', 'date_created', 'employment']
    list_display = ['eid', 'person', 'employment', 'is_active']
    permission_helper_class = EmployeeDataPermissionHelper
    create_view_class = EmployeeCreateView

    employee_panels = [

        MultiFieldPanel([
            FieldPanel('eid'),
            AutocompletePanel('person'),
            AutocompletePanel('department'),
            FieldPanel('employment'),
            DocumentChooserPanel('attachment'),
            FieldPanel('is_active'),
        ]),
        InlinePanel(
            'chairs', label=_('Chairs'),
            panels=[
                FieldPanel('chair'),
                DocumentChooserPanel('attachment'),
                FieldPanel('is_primary'),
                FieldPanel('is_active')
            ]
        )
    ]

    edit_handler = TabbedInterface([
        ObjectList(employee_panels, heading=_('Basic Information'))
    ])


class DepartmentModelAdmin(ModelAdmin):
    model = Department
    menu_icon = ' icon-fa-sitemap'
    search_fields = ['name']
    list_filter = ['level']
    list_display = ['name', 'parent']

    panels = [
        MultiFieldPanel([
            FieldPanel('parent'),
            FieldPanel('name')
        ]),
    ]

    def get_queryset(self, request):
        return self.model.objects.all()

    def get_ordering(self, request):
        """
        Changes the default ordering for changelists to tree-order.
        """
        mptt_opts = self.model._mptt_meta
        return self.ordering or (mptt_opts.tree_id_attr, mptt_opts.left_attr)


class ChairModelAdmin(ModelAdmin):
    model = Chair
    menu_icon = ' icon-fa-briefcase'
    search_fields = ['position', 'department__name']
    list_filter = ['department__level']
    list_display = ['position', 'department', 'description']

    basic_panels = [
        MultiFieldPanel([
            FieldPanel('parent'),
            FieldPanel('position'),
            FieldPanel('department'),
            FieldPanel('is_single'),
            FieldPanel('employee_required'),
            DocumentChooserPanel('attachment'),
            FieldPanel('description'),
        ]),
    ]

    edit_handler = TabbedInterface([
        ObjectList(basic_panels, heading=_('Basic Information'))
    ])



class DashboardView(TemplateView):
    template_name = 'modeladmin/employees/dashboard.html'


class HumanResourceGroup(ModelAdminGroup):
    menu_label = _('Human Resource')
    menu_icon = 'group'
    items = [PersonAsEmployeeModelAdmin, EmployeeModelAdmin, DepartmentModelAdmin, ChairModelAdmin]

    def get_submenu_items(self):
        items = super().get_submenu_items()

        # TODO Next update
        # dashboard_menu = MenuItem(
        #     label='Dashboard', url=reverse('employees_dashboard'),
        #     classnames='icon icon-fa-dashboard', order=0
        # )
        # items.append(dashboard_menu)

        return items


modeladmin_register(HumanResourceGroup)
