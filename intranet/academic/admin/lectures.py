from django.utils import translation
from django.shortcuts import reverse

from wagtail.admin.menu import MenuItem
from wagtail.contrib.modeladmin.options import ModelAdminGroup

from wagtailkit.lectures.admin import (
    LectureModelAdmin,
    LectureScoreModelAdmin,
    LectureScheduleModelAdmin,
    LectureScoreWeightingModelAdmin
)

from wagtailkit.attendances.admin import (
    StudentAttendanceModelAdmin,
    TeacherAttendanceModelAdmin
)

_ = translation.gettext_lazy


class LectureModelAdminGroup(ModelAdminGroup):
    menu_label = _('Lectures')
    menu_icon = 'fa-slideshare'
    items = [
        LectureModelAdmin,
        LectureScheduleModelAdmin,
        StudentAttendanceModelAdmin,
        TeacherAttendanceModelAdmin,
        LectureScoreWeightingModelAdmin,
        LectureScoreModelAdmin
    ]