from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EvaluationsConfig(AppConfig):
    name = 'wagtailkit.evaluations'
    verbose_name = _('Wagtailkit Evaluations')
