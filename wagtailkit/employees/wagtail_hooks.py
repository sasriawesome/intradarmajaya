from django.contrib.auth import get_permission_codename
from wagtail.admin.navigation import get_site_for_user
from wagtail.admin.site_summary import SummaryItem
from wagtail.core import hooks

from wagtail.contrib.modeladmin.helpers import PermissionHelper
from .models import Employee

class EmployeeWelcomePanel(SummaryItem):
    order = 50
    template = 'modeladmin/employees/admin_homepage_summary.html'
    ph = PermissionHelper(Employee)

    def get_context(self):
        site_name = get_site_for_user(self.request.user)['site_name']
        summary = Employee.objects.get_summary()
        return {
            'site_name': site_name,
            'summary': summary
        }

    def is_shown(self):
        has_perm = self.ph.user_has_any_permissions(self.request.user)
        return has_perm



@hooks.register('construct_homepage_panels')
def add_employee_welcome_panel(request, panels):
    panel = EmployeeWelcomePanel(request)
    if panel.is_shown():
        panels.append(panel)
