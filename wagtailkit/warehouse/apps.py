from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WarehouseConfig(AppConfig):
    name = 'wagtailkit.warehouse'
    verbose_name = _('Wagtailkit Warehouse')
