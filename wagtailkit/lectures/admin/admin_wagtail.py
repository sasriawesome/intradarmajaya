from django.utils import translation
from wagtail.admin.edit_handlers import (
    ObjectList, TabbedInterface, FieldPanel,
    MultiFieldPanel, InlinePanel, FieldRowPanel)
from wagtail.contrib.modeladmin.options import ModelAdmin

from wagtailkit.admin.helpers import ButtonHelper
from wagtailkit.autocompletes.edit_handlers import AutocompletePanel
from wagtailkit.academic.admin import ProgramStudyFilter
from wagtailkit.lectures.models import (
    Lecture, LectureScore,
    LectureSchedule,
    LectureScoreWeighting
)

_ = translation.gettext_lazy

LIST_PER_PAGE = 20


class LectureButtonHelper(ButtonHelper):
    buttons_exclude = []


class LectureModelAdmin(ModelAdmin):
    model = Lecture
    menu_icon = 'fa-share-square-o'
    menu_label = _('Lectures')
    inspect_view_enabled = True
    button_helper_class = LectureButtonHelper
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


class LectureScoreModelAdmin(ModelAdmin):
    list_per_page = LIST_PER_PAGE
    menu_label = _('Scores')
    menu_icon = 'fa-wpforms'
    search_fields = ['student__name', 'course__name', 'lecture__teacher__employee__person__fullname']
    list_filter = ['student__rmu']
    list_display = ['student', 'course', 'lecture', 'total_score', 'numeric', 'alphabetic']
    model = LectureScore
    edit_handler = ObjectList([
        MultiFieldPanel([
            AutocompletePanel('lecture'),
            AutocompletePanel('student'),
        ]),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('homework1'),
                FieldPanel('homework2'),
            ]),
            FieldRowPanel([
                FieldPanel('quis1'),
                FieldPanel('quis2'),
            ]),
            FieldRowPanel([
                FieldPanel('mid_exam'),
                FieldPanel('final_exam'),
            ]),
            FieldRowPanel([
                FieldPanel('attendance'),
                FieldPanel('total_score'),
            ]),
            FieldRowPanel([
                FieldPanel('numeric'),
                FieldPanel('alphabetic'),
            ])
        ], heading=_('Scores'))
    ])


class LectureScheduleModelAdmin(ModelAdmin):
    menu_icon = 'fa-calendar'
    menu_label = _('Schedules')
    model = LectureSchedule
    search_fields = [
        'lecture__course__course__name',
        'room__name', 'room__code',
        'lecture__teacher__employee__person__fullname'
    ]
    list_display = ['lecture', 'session', 'room', 'date', 'time_start', 'time_end', 'type']
    list_filter = ['date', 'type', 'lecture__rmu']
    edit_handler = ObjectList([
        MultiFieldPanel([
            AutocompletePanel('lecture'),
            AutocompletePanel('room'),
            FieldPanel('type'),
            FieldRowPanel([
                FieldPanel('session'),
                FieldPanel('date'),
            ]),
            FieldRowPanel([
                FieldPanel('time_start'),
                FieldPanel('time_end'),
            ])
        ])
    ])

class LectureScoreWeightingModelAdmin(ModelAdmin):
    menu_icon = 'fa-wpforms'
    menu_label = _('Weighting')
    model = LectureScoreWeighting
    search_fields = [
        'lecture__course__course__name'
        'lecture__teacher__employee__person__fullname'
    ]
    list_filter = ['lecture__rmu']

    edit_handler = ObjectList([
        MultiFieldPanel([
            AutocompletePanel('lecture'),
            FieldRowPanel([
                FieldPanel('attendance'),
                FieldPanel('homework1'),
                FieldPanel('homework2'),
            ]),
            FieldRowPanel([
                FieldPanel('quis1'),
                FieldPanel('quis2'),
            ]),
            FieldRowPanel([
                FieldPanel('mid_exam'),
                FieldPanel('final_exam'),
            ]),
        ])
    ])
