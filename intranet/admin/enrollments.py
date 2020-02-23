from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdminGroup
from wagtailkit.enrollments.admin import EnrollmentModelAdmin


class EnrollmentModelAdminGroup(ModelAdminGroup):
    menu_icon = 'fa-wpforms'
    menu_label = _('Enrollments')
    items = [
        EnrollmentModelAdmin
    ]