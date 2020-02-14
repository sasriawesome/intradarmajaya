from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.shortcuts import redirect, reverse

from wagtail.admin.edit_handlers import ObjectList, TabbedInterface, FieldPanel, MultiFieldPanel
from wagtailkit.admin.admin import ModelAdmin
from wagtailkit.persons.admin import PersonModelAdmin
from wagtailkit.employees.admin import EmployeeModelAdmin
from wagtailkit.teachers.models import Teacher, TeacherPersonal, TeacherEmployment
from wagtailkit.academic.admin.admin_wagtail import ProgramStudyFilter


class TeacherEmploymentModelAdmin(EmployeeModelAdmin):
    inspect_view_enabled = True
    model = TeacherEmployment
    menu_icon = 'fa-user'
    menu_label = _('Teacher Employment')


class TeacherPersonalModelAdmin(PersonModelAdmin):
    model = TeacherPersonal
    menu_icon = 'fa-user'
    menu_label = _('Teacher Personal')


class TeacherModelAdmin(ModelAdmin):
    model = Teacher
    menu_icon = 'fa-user'
    inspect_view_enabled = True
    list_filter = ['is_active', ProgramStudyFilter]
    search_fields = ['tid', 'employee__person__fullname', 'rmu__name']
    list_display = ['tid', 'name', 'rmu', 'is_active']
    edit_handler = ObjectList([
        MultiFieldPanel([
            FieldPanel('tid'),
            FieldPanel('is_nidn'),
            FieldPanel('employee'),
            FieldPanel('rmu'),
            FieldPanel('courses'),
            FieldPanel('is_active')
        ])
    ], heading=_('Student'))
