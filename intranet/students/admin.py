from django.utils import translation, html
from django.conf.urls import url
from django.shortcuts import get_object_or_404, redirect, reverse

from wagtail.admin.messages import messages
from wagtail.admin.edit_handlers import MultiFieldPanel, ObjectList, FieldPanel
from wagtail.contrib.modeladmin.options import ModelAdminGroup, modeladmin_register
from wagtail.contrib.modeladmin.helpers import ButtonHelper, AdminURLHelper
from wagtail.contrib.modeladmin.views import EditView
from wagtailkit.admin.admin import ModelAdmin
from wagtailkit.admin.helpers import PermissionHelper
from wagtailkit.lectures.models import LectureStatus

from .models import (
    LectureForStudent, ScheduleForStudent, ScoreForStudent,
    StudentEnrollment, StudentEnrollmentPlan, LectureOffered
)

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


class StudentEnrollmentModelAdmin(ModelAdmin):
    menu_label = _('Enrollments')
    menu_icon = 'fa-wpforms'
    model = StudentEnrollment


class EnrollmentPlanPermissionHelper(PermissionHelper):
    """ Restrict for add or delete lecture from plan """

    def user_can_create(self, user):
        return False

    def user_can_edit_obj(self, user, obj):
        return True


class PlanEditView(EditView):
    pass


class StudentEnrollmentPlanModelAdmin(ModelAdmin):
    menu_label = _('Plans')
    menu_icon = 'fa-navicon'
    permission_helper_class = EnrollmentPlanPermissionHelper
    edit_view_class = PlanEditView
    inspect_view_enabled = True
    model = StudentEnrollmentPlan
    list_display = ['course_name', 'academic_year', 'series', 'location', 'sks', 'criteria']

    edit_handler = ObjectList([
        MultiFieldPanel([
            FieldPanel('criteria')
        ])
    ])

    def academic_year(self, obj):
        return obj.lecture.academic_year

    def sks(self, obj):
        return "{} SKS".format(obj.lecture.course.sks_total)

    def series(self, obj):
        return "{} * {} Mnt".format(obj.lecture.series, obj.lecture.duration)

    def course_name(self, obj):
        obj = obj.lecture
        return html.format_html("{} <br/>{}<br/>{}".format(
            obj.code, obj.course, obj.teacher))

    def location(self, obj):
        obj = obj.lecture
        return html.format_html("{}<br/>{} {}".format(obj.room, obj.date_start, obj.default_time_start))

    def get_queryset(self, request):
        qs = self.model.objects.all()
        if request.user.is_superuser:
            return qs
        student = getattr(request.user.person, 'student', None)
        if student:
            return qs.filter(student=student)
        else:
            return


class LectureOfferedButtonHelper(ButtonHelper):
    def get_buttons_for_obj(self, obj, **kwargs):
        btns = super().get_buttons_for_obj(obj, **kwargs)
        btns.append({
            'url': self.url_helper.get_action_url('add_to_plan', obj.id),
            'label': _('Add to Plan'),
            'classname': '',
            'title': _('Add this %s to plan') % self.verbose_name,
        })
        return btns


class LectureOfferedCatalogue(ModelAdmin):
    menu_icon = 'fa-navicon'
    menu_label = _("Lectures")
    model = LectureOffered
    button_helper_class = LectureOfferedButtonHelper
    inspect_view_enabled = True
    search_fields = [
        'course__course__name',
        'teacher__employee__person__fullname']
    list_display = ['course_name', 'academic_year', 'sessions', 'location', 'sks', 'status']

    def get_admin_urls_for_registration(self):
        urls = super().get_admin_urls_for_registration()
        urls += (
            url(self.url_helper.get_action_url_pattern('add_to_plan'),
                self.add_to_plan_view,
                name=self.url_helper.get_action_url_name('add_to_plan')),
        )

        return urls

    def sks(self, obj):
        return "{} SKS".format(obj.course.sks_total)

    def course_name(self, obj):
        return html.format_html(
            "{} {}<br/>{}".format(obj.code, obj.course, obj.teacher))

    def sessions(self, obj):
        return "{} * {} Mnt".format(obj.series, obj.duration)

    def location(self, obj):
        return html.format_html("{}<br/>{} {}".format(obj.room, obj.date_start, obj.default_time_start))

    def get_queryset(self, request):
        qs = self.model.objects.filter(status=LectureStatus.REGISTRATION.value)
        if request.user.is_superuser:
            return qs
        student = getattr(request.user.person, 'student', None)
        if student:
            student_plan = [plan.lecture.id for plan in StudentEnrollmentPlan.objects.filter(student=student)]
            return qs.filter(rmu=student.rmu).exclude(id__in=student_plan)
        else:
            return

    def add_to_plan_view(self, request, instance_pk):
        instance = get_object_or_404(self.model, pk=instance_pk)
        # add to plan
        defaults = {
            'student': request.user.person.student,
            'lecture': instance,
            'creator': request.user
        }
        StudentEnrollmentPlan.objects.get_or_create(
            **defaults, defaults=defaults
        )
        messages.add_message(request, messages.SUCCESS, _("{} added to your plan").format(instance))
        return redirect(reverse(self.url_helper.get_action_url_name('index')))


class StudentDasboardAdminGroup(ModelAdminGroup):
    menu_order = 1
    menu_label = _("Student Area")
    menu_icon = 'fa-trello'
    items = [
        StudentLectureModelAdmin,
        StudentScheduleModelAdmin,
        StudentScoreModelAdmin
    ]


class EnrollmentAdminGroup(ModelAdminGroup):
    menu_label = _("Enrollments")
    menu_icon = 'fa-wpforms'
    items = [
        StudentEnrollmentModelAdmin,
        LectureOfferedCatalogue,
        StudentEnrollmentPlanModelAdmin
    ]

modeladmin_register(StudentDasboardAdminGroup)
modeladmin_register(EnrollmentAdminGroup)
