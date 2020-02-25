from wagtail.contrib.modeladmin.options import modeladmin_register
from .academic import *
from .lectures import *
from .students import *
from .teachers import *
from .rooms import *
from .enrollments import *

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


class TeacherModelAdminGroup(ModelAdminGroup):
    menu_order = 103
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


class StudentModelAdminGroup(ModelAdminGroup):
    menu_order = 104
    menu_label = _('Students')
    menu_icon = 'fa-user-circle'
    items = [
        StudentModelAdmin,
        StudentPersonalModelAdmin,
        StudentScoreModelAdmin,
        ConversionScoreModelAdmin,
    ]

    def get_submenu_items(self):
        sub_menuitems = super().get_submenu_items()
        register_student_menu = RegisterStudentMenuItem(
            _('Registration'),
            reverse('modeladmin_register_student'),
            classnames='icon icon-fa-user-plus', order=1000)
        sub_menuitems.append(register_student_menu)
        return sub_menuitems


class EnrollmentModelAdminGroup(ModelAdminGroup):
    menu_icon = 'fa-wpforms'
    menu_label = _('Enrollments')
    items = [
        EnrollmentModelAdmin
    ]


modeladmin_register(AcademicModelAdminGroup)
modeladmin_register(CourseGroupModelAdmin)
modeladmin_register(StudentModelAdminGroup)
modeladmin_register(TeacherModelAdminGroup)
modeladmin_register(LectureModelAdminGroup)
modeladmin_register(EnrollmentModelAdminGroup)
