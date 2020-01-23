from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WagtailkitEmployeesConfig(AppConfig):
    name = 'wagtailkit.employees'
    verbose_name = _("Wagtailkit Employees")