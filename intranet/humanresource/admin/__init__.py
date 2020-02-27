from django.utils import translation
from django.shortcuts import reverse

from wagtail.admin.menu import MenuItem
from wagtail.contrib.modeladmin.options import (
    ModelAdminGroup, modeladmin_register
)

from wagtailkit.organizations.admin import DepartmentModelAdmin, PositionModelAdmin

from .person import PersonModelAdmin

from .employee import (
    EmployeePersonalModelAdmin,
    EmploymentModelAdmin,
    EmployeeModelAdmin,
)

_ = translation.gettext_lazy


class PersonsModelAdminGroup(ModelAdminGroup):
    menu_order = 101
    menu_icon = 'fa-user-circle'
    menu_label = _('Persons')
    items = [
        PersonModelAdmin
    ]


class EmployeesAdminGroup(ModelAdminGroup):
    menu_order = 102
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
    menu_label = _('HR Management')
    menu_icon = 'group'
    items = [
        DepartmentModelAdmin,
        PositionModelAdmin
    ]

    def get_submenu_items(self):
        items = super().get_submenu_items()
        return items


modeladmin_register(PersonsModelAdminGroup)
modeladmin_register(EmployeesAdminGroup)
modeladmin_register(HumanResourceAdminGroup)
