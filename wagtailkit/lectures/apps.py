from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LecturesConfig(AppConfig):
    name = 'wagtailkit.lectures'
    verbose_name = _('Wagtailkit Lectures')
