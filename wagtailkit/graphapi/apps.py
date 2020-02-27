from django.apps import AppConfig


class GraphapiConfig(AppConfig):
    name = 'wagtailkit.graphapi'
    label = 'wagtailkit_graphapi'
    verbose_name = 'Wagtailkit GraphQL API'

    def ready(self):
        super().ready()
        self.module.autodiscover()