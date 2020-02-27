from django.conf.urls import url
from wagtail.admin.auth import require_admin_access

from wagtailkit.autocompletes.views import create, objects, search


urlpatterns = [
    url(r'^create/', require_admin_access(create)),
    url(r'^objects/', require_admin_access(objects)),
    url(r'^search/', require_admin_access(search)),
]
