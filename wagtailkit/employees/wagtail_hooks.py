from django.conf.urls import url
from wagtail.core import hooks

from wagtailkit.employees.admin.admin_wagtail import DashboardView

@hooks.register('register_admin_urls')
def urlconf_time():
  return [
    url(r'^employees/dashboard/$', DashboardView.as_view(), name='employees_dashboard'),
  ]