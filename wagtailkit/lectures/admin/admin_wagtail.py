from django.utils import translation, html
from django.contrib import admin

from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.admin.edit_handlers import (
    ObjectList, TabbedInterface, FieldPanel, RichTextFieldPanel,
    MultiFieldPanel, InlinePanel, FieldRowPanel)
from wagtail.contrib.modeladmin.options import ModelAdmin

from wagtailkit.autocompletes.edit_handlers import AutocompletePanel
from wagtailkit.academic.admin import RMUChooser, ProgramStudyFilter
from wagtailkit.teachers.admin import TeacherChooser
from wagtailkit.lectures.models import Lecture

_ = translation.gettext_lazy

LIST_PER_PAGE = 20


class LectureModelAdmin(ModelAdmin):
    model = Lecture
    menu_icon = 'fa-share-square-o'
    menu_label = _('Lectures')
    list_per_page = LIST_PER_PAGE
    search_fields = ['teacher__employee__person__fullname', 'course__course__name']
    list_display = ['code', 'teacher', 'course', 'room']
    list_filter = ['status', ProgramStudyFilter, 'academic_year']

    def course_name(self, obj):
        return obj.course.course_name

    course_panels = [
        MultiFieldPanel([
            FieldPanel('code'),
            FieldPanel('academic_year'),
            AutocompletePanel('rmu'),
            AutocompletePanel('course'),
            AutocompletePanel('teacher'),
            AutocompletePanel('assistant'),
        ])
    ]
    datetime_panels = [
        MultiFieldPanel([
            AutocompletePanel('room'),
            FieldPanel('date_start'),
            FieldPanel('default_time_start'),
            FieldPanel('duration'),
            FieldPanel('series'),
            FieldPanel('status'),
        ])
    ]
    student_panels = [
        InlinePanel('students', panels=[
            AutocompletePanel('student'),
            FieldPanel('status')
        ])
    ]

    edit_handler = TabbedInterface([
        ObjectList(course_panels, heading=_('Course')),
        ObjectList(datetime_panels, heading=_('Date & Time')),
        ObjectList(student_panels, heading=_('Students')),
    ])
