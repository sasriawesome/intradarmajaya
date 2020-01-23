import copy
import os
from importlib import import_module
from django.utils.module_loading import module_has_submodule
from .graphql import graphql_schema

default_app_config = 'wagtailkit.api.apps.ApiConfig'


def custom_autodiscover_modules(*args, **kwargs):
    """
    Auto-discover INSTALLED_APPS modules and fail silently when
    not present. This forces an import on them to register any admin bits they
    may want.

    You may provide a register_to keyword parameter as a way to access a
    registry. This register_to object must have a _registry instance variable
    to access it.
    """
    from django.apps import apps

    register_to = kwargs.get('register_to')
    for app_config in apps.get_app_configs():
        for module_to_search in args:
            try:
                import_module('%s.%s' % (app_config.name, module_to_search))
            except Exception:
                if module_has_submodule(app_config.module, module_to_search):
                    raise

def autodiscover():
    custom_autodiscover_modules('schemas', register_to=graphql_schema)
