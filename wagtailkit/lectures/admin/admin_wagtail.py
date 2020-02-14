from django.utils import translation, html
from django.contrib import admin

from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.admin.edit_handlers import (
    ObjectList, TabbedInterface, FieldPanel, RichTextFieldPanel,
    MultiFieldPanel, InlinePanel, FieldRowPanel)
from wagtail.contrib.modeladmin.options import ModelAdmin

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
            FieldPanel('course'),
            FieldRowPanel([
                FieldPanel('rmu'),
                FieldPanel('academic_year'),
            ]),
            FieldRowPanel([
                FieldPanel('teacher'),
                FieldPanel('assistant'),
            ])
        ])
    ]
    datetime_panels = [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('room'),
                FieldPanel('date_start'),
            ]),
            FieldRowPanel([
                FieldPanel('default_time_start'),
                FieldPanel('duration'),
            ]),
            FieldRowPanel([
                FieldPanel('series'),
                FieldPanel('status'),
            ])
        ])
    ]

    edit_handler = TabbedInterface([
        ObjectList(course_panels, heading=_('Course')),
        ObjectList(datetime_panels, heading=_('Date & Time')),
    ])
