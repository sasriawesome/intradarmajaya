from django.utils import translation
from django.shortcuts import reverse

from wagtail.admin.menu import MenuItem
from wagtail.contrib.modeladmin.options import ModelAdminGroup

from wagtailkit.academic.admin import (
    CourseGroupModelAdmin,
    CourseTypeModelAdmin,
    CourseModelAdmin,
    SyllabusModelAdmin,
    CurriculumModelAdmin,
    ResourceManagementUnitModelAdmin,
    AcademicYearModelAdmin,
    AcademicActivityModelAdmin,
    SchoolYearModelAdmin
)

from wagtailkit.students.admin import StudentModelAdmin, StudentPersonalModelAdmin, RegisterStudentMenuItem
from wagtailkit.lectures.admin import LectureModelAdmin

_ = translation.gettext_lazy


class AcademicModelAdminGroup(ModelAdminGroup):
    menu_label = _('Academic')
    menu_icon = 'fa-mortar-board'
    items = [
        ResourceManagementUnitModelAdmin,
        AcademicYearModelAdmin,
        SchoolYearModelAdmin,
        SyllabusModelAdmin,
        AcademicActivityModelAdmin,
    ]


class CourseModelAdminGroup(ModelAdminGroup):
    menu_label = _('Courses')
    menu_icon = 'fa-book'
    items = [
        CurriculumModelAdmin,
        CourseModelAdmin,
        CourseGroupModelAdmin,
        CourseTypeModelAdmin
    ]


class StudentModelAdminGroup(ModelAdminGroup):
    menu_label = _('Students')
    menu_icon = 'fa-user-circle'
    items = [
        StudentModelAdmin,
        StudentPersonalModelAdmin
    ]

    def get_submenu_items(self):
        sub_menuitems = super().get_submenu_items()
        register_student_menu = RegisterStudentMenuItem(
            _('Registration'),
            reverse('modeladmin_register_student'),
            classnames='icon icon-fa-user-plus', order=1000)
        sub_menuitems.append(register_student_menu)
        return sub_menuitems


class LectureModelAdminGroup(ModelAdminGroup):
    menu_label = _('Lectures')
    menu_icon = 'fa-slideshare'
    items = [
        LectureModelAdmin
    ]
