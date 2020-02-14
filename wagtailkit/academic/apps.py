from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AcademicConfig(AppConfig):
    name = 'wagtailkit.academic'
    verbose_name = _("Wagtailkit Academic")
