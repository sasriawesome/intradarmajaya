from django.utils import translation
from django.shortcuts import reverse

from wagtail.admin.menu import MenuItem
from wagtail.contrib.modeladmin.options import (ModelAdminGroup, modeladmin_register)

from wagtailkit.organizations.admin import DepartmentModelAdmin, PositionModelAdmin

from wagtailkit.employees.admin import (
    EmployeePersonalModelAdmin,
    EmploymentModelAdmin,
    EmployeeModelAdmin,
)


_ = translation.gettext_lazy

class EmployeesAdminGroup(ModelAdminGroup):
    menu_label = _('Employees')
    menu_icon = 'fa-user-circle'
    items = [
        EmployeeModelAdmin,
        EmployeePersonalModelAdmin,
        EmploymentModelAdmin,
    ]

    def get_submenu_items(self):
        items = super().get_submenu_items()
        return items


class HumanResourceAdminGroup(ModelAdminGroup):
    menu_label = _('HRD')
    menu_icon = 'group'
    items = [
        DepartmentModelAdmin,
        PositionModelAdmin
    ]

    def get_submenu_items(self):
        items = super().get_submenu_items()
        return items
