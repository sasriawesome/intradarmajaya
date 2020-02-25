from django.utils import translation, html
from django.shortcuts import reverse

from wagtail.admin.menu import MenuItem
from wagtail.contrib.modeladmin.options import ModelAdminGroup
from wagtail.contrib.modeladmin.helpers import PermissionHelper
from wagtailkit.admin.admin import ModelAdmin

from intranet.models import LectureForStudent, ScheduleForStudent, ScoreForStudent

_ = translation.gettext_lazy


class ReadOnlyPermission(PermissionHelper):
    """ Make suer admin read only """

    def user_can_create(self, user):
        return False

    def user_can_delete_obj(self, user, obj):
        return False

    def user_can_edit_obj(self, user, obj):
        return False


class StudentLectureModelAdmin(ModelAdmin):
    menu_label = _('Lectures')
    menu_icon = 'fa-slideshare'
    inspect_view_enabled = True
    model = LectureForStudent
    permission_helper_class = ReadOnlyPermission
    search_fields = [
        'course__course__name',
        'teacher__employee__person__fullname']
    list_filter = ['academic_year', 'status']
    list_display = ['course_name', 'academic_year', 'series', 'location', 'status']

    def course_name(self, obj):
        return html.format_html("{}<br/>{}<br/>{}".format(obj.code, obj.course, obj.teacher))

    def location(self, obj):
        return html.format_html("{}<br/>{}".format(obj.room, obj.date_start))

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        student = getattr(request.user.person, 'student', None)
        if student:
            return qs.filter(students__student=student)
        else:
            return


class StudentScheduleModelAdmin(ModelAdmin):
    menu_label = _('Schedules')
    menu_icon = 'fa-calendar'
    inspect_view_enabled = True
    permission_helper_class = ReadOnlyPermission
    model = ScheduleForStudent
    search_fields = ['lecture__code',
                     'lecture__teacher__employee__person__fullname',
                     'lecture__course__course__name']
    list_filter = ['date', 'type']
    list_display = ['date_time', 'course_name', 'room', 'session', 'is_open']

    def is_open(self, obj):
        return obj.status

    is_open.boolean = True

    def course_name(self, obj):
        return html.format_html("{}<br/>{}<br/>{}".format(obj.lecture.code, obj.lecture.course, obj.lecture.teacher))

    def date_time(self, obj):
        return html.format_html("{}<br/>{} - {}".format(obj.date, obj.time_start, obj.time_end))

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        student = getattr(request.user.person, 'student', None)
        if student:
            return qs.filter(lecture__students__student=student)
        else:
            return


class StudentScoreModelAdmin(ModelAdmin):
    menu_label = _('Score')
    menu_icon = 'fa-wpforms'
    model = ScoreForStudent
    inspect_view_enabled = True
    permission_helper_class = ReadOnlyPermission
    search_fields = ['course__course__name']
    list_filter = ['alphabetic', 'course__curriculum']
    list_display = ['code', 'course', 'curriculum', 'numeric', 'alphabetic']

    def code(self, obj):
        return obj.course.course.inner_id

    def curriculum(self, obj):
        return obj.course.curriculum

    def get_queryset(self, request):
        qs = self.model.alt_manager.all()
        if request.user.is_superuser:
            return qs
        student = getattr(request.user.person, 'student', None)
        if student:
            return qs.filter(student=student)
        else:
            return

class StudentDasboardAdminGroup(ModelAdminGroup):
    menu_label = _("Student Area")
    menu_icon = 'fa-trello'
    items = [
        StudentLectureModelAdmin,
        StudentScheduleModelAdmin,
        StudentScoreModelAdmin
    ]
