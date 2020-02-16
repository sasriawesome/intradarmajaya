from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdminGroup
from wagtailkit.teachers.admin import TeacherModelAdmin, TeacherPersonalModelAdmin, TeacherEmploymentModelAdmin

class TeacherModelAdminGroup(ModelAdminGroup):
    menu_label = _('Teachers')
    menu_icon = 'fa-user-circle'
    items = [
        TeacherModelAdmin,
        TeacherPersonalModelAdmin,
        TeacherEmploymentModelAdmin
    ]

    def get_submenu_items(self):
        sub_menuitems = super().get_submenu_items()
        return sub_menuitems