from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OrganizationsConfig(AppConfig):
    name = 'wagtailkit.organizations'
    verbose_name = _("Wagtailkit Organizations")