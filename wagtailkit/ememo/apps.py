from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EmemoConfig(AppConfig):
    name = 'wagtailkit.ememo'
    verbose_name = _('Wagtailkit E-Memo')
