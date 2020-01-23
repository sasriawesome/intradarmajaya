from django.utils.translation import gettext_lazy as _

from zerp_core.admin import (
    ModelAdminBase, TabularInlineBase, ReadOnlyModelAdmin)
from zerp_lecture.models import (
    Lecture, LectureSchedule, LectureStudentAttendant, LectureStudent,
    StudentScore, LectureScoreWeighting, LectureTeacherAttendant)
from .forms import LectureForm


class LectureScoreWeightInline(TabularInlineBase):
    extra = 0
    model = LectureScoreWeighting
    exclude = ['created_by', 'modified_by', 'date_created', 'date_modified']

class LectureSceduleInline(TabularInlineBase):
    extra = 0
    model = LectureSchedule
    readonly_fields = ['inner_id']
    exclude = ['reg_number', 'inner_id', 'created_by', 'modified_by', 'date_created', 'date_modified']
    ordering = ('edate',)

    def get_max_num(self, request, obj=None, **kwargs):
        """ Set max num based on order_item.order_qty """
        try:
            kwarg = request.resolver_match.kwargs
            parent_id = kwarg.get('object_id')
            parent = Lecture.objects.get(pk=parent_id)
            return parent.series
        except Exception:
            return super().get_max_num(request, obj=obj)


class LectureAdmin(ModelAdminBase):
    inlines = [LectureScoreWeightInline, LectureSceduleInline]
    exclude = ['created_by', 'modified_by', 'date_created', 'date_modified', 'reg_number', 'inner_id']
    search_fields = [
        'teacher_course__inner_id',
        'teacher_course__teacher__person__name']
    list_display = [
        'inner_id', 'teacher_course', 'duration', 'series',
        'status', 'default_time_start', 'time_end']

    def time_end(self, obj):
        return obj.default_time_end

    time_end.short_description = _('Time end')


class LectureScoreWeigtingAdmin(ModelAdminBase):
    list_select_related = ['lecture']
    search_fields = ['lecture__inner_id']
    list_display = [
        'lecture', 'attendance', 'homework1', 'homework2', 'quis1', 'quis2',
        'mid_exam', 'final_exam', 'total']


class StudentScoreAdmin(ModelAdminBase):
    list_select_related = ['lecture_student']
    search_fields = ['lecture_student__student__person__firstname']
    exclude = ['created_by', 'modified_by', 'date_created', 'date_modified']
    list_display = [
        'lecture_student', 'homework1', 'homework2', 'quis1',
        'quis2', 'mid_exam', 'final_exam']


class LectureStudentAttendanceInline(TabularInlineBase):
    extra = 0
    model = LectureStudentAttendant


class LectureTeacherAttendanceInline(TabularInlineBase):
    extra = 0
    max_num = 2
    model = LectureTeacherAttendant


class LectureStudentAttendanceAdmin(ReadOnlyModelAdmin, ModelAdminBase):
    date_hierarchy = 'edate'
    inlines = [LectureTeacherAttendanceInline, LectureStudentAttendanceInline]
    exclude = ['created_by', 'modified_by', 'date_created', 'date_modified']
    search_fields = [
        'lecture__teacher_course__teacher__person__firstname']
    list_display = [
        'inner_id', 'lecture', 'room', 'edate', 'time_start',
        'time_end', 'status_label']
    fieldsets = (
        (str(_('Lecture')).upper(), {
            # 'classes': ('silabis-admin-fieldset',),
            'fields': (
                'inner_id', 'lecture',
                ('edate', 'room', 'time_start', 'time_end', 'status_label')
            ),
        }),)

    def status_label(self, obj):
        return obj.status

    status_label.short_description = _("Open")
    status_label.boolean = True


class LectureStudentScoreInline(TabularInlineBase):
    extra = 0
    model = StudentScore


class LectureStudentScoreAdmin(ReadOnlyModelAdmin, ModelAdminBase):
    form = LectureForm
    inlines = [LectureStudentScoreInline]
    search_fields = [
        'teacher_course__inner_id',
        'teacher_course__teacher__person__name']
    list_display = [
        'inner_id', 'teacher_course', 'duration', 'series',
        'status', 'default_time_start', 'time_end']
    fieldsets = (
        (str(_('Lecture')).upper(), {
            # 'classes': ('silabis-admin-fieldset',),
            'fields': ('inner_id', 'teacher_course'),
        }),)

    def time_end(self, obj):
        return obj.default_time_end

    time_end.short_description = _('Time end')


