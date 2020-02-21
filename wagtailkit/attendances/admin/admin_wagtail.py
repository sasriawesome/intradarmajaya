from django.utils import translation
from wagtail.admin.edit_handlers import (
    ObjectList, TabbedInterface, FieldPanel,
    MultiFieldPanel, InlinePanel, FieldRowPanel)
from wagtail.contrib.modeladmin.options import ModelAdmin

from wagtailkit.admin.helpers import ButtonHelper
from wagtailkit.autocompletes.edit_handlers import AutocompletePanel
from wagtailkit.academic.admin import ProgramStudyFilter
from wagtailkit.attendances.models import (
    StudentAttendance,
    TeacherAttendance,
    LectureAttendance
)

_ = translation.gettext_lazy

LIST_PER_PAGE = 20


class StudentAttendanceModelAdmin(ModelAdmin):
    model = StudentAttendance
    menu_icon = 'fa-hand-pointer-o'
    menu_label = _('Student Attendance')
    inspect_view_enabled = True
    list_per_page = LIST_PER_PAGE
    search_fields = ['student__student__person__fullname', 'schedule__lecture__name']
    list_display = ['schedule', 'student', 'status', 'note']
    list_filter = ['status', ProgramStudyFilter]

    edit_handler = ObjectList([
            MultiFieldPanel([
                AutocompletePanel('student'),
                AutocompletePanel('schedule'),
                FieldPanel('status'),
                FieldPanel('note'),
            ])
        ])

class TeacherAttendanceModelAdmin(ModelAdmin):
    model = TeacherAttendance
    menu_icon = 'fa-hand-pointer-o'
    menu_label = _('Teacher Attendance')
    inspect_view_enabled = True
    list_per_page = LIST_PER_PAGE
    search_fields = ['teacher__employee__person__fullname', 'schedule__lecture__name']
    list_display = ['schedule', 'teacher', 'status', 'note']
    list_filter = ['status', ProgramStudyFilter]

    edit_handler = ObjectList([
            MultiFieldPanel([
                AutocompletePanel('teacher'),
                AutocompletePanel('schedule'),
                FieldPanel('status'),
                FieldPanel('note'),
            ])
        ])