from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'wagtailkit.api'
    label = 'wagtailkitapi'
    verbose_name = 'Wagtailkit API'

    def ready(self):
        super().ready()
        self.module.autodiscover()