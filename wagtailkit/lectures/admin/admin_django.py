from django.contrib import admin

from wagtailkit.lectures.models import (
    Lecture, LectureStudent, LectureScoreWeighting,
    LectureSchedule, StudentScore, LectureScore)


class LectureScoreWeightInline(admin.TabularInline):
    extra = 0
    model = LectureScoreWeighting
    exclude = ['created_by', 'modified_by', 'date_created', 'date_modified']


class LectureSceduleInline(admin.TabularInline):
    extra = 0
    model = LectureSchedule
    raw_id_fields = ['room']
    ordering = ('date',)

    def get_max_num(self, request, obj=None, **kwargs):
        """ Set max num based on order_item.order_qty """
        try:
            kwarg = request.resolver_match.kwargs
            parent_id = kwarg.get('object_id')
            parent = Lecture.objects.get(pk=parent_id)
            return parent.series
        except Exception:
            return super().get_max_num(request, obj=obj)


class LectureStudentInline(admin.TabularInline):
    extra = 0
    model = LectureStudent
    raw_id_fields = ['student']


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    search_fields = ['teacher__person__fullname', 'course__name']
    inlines = [LectureScoreWeightInline, LectureStudentInline, LectureSceduleInline]
    list_display = ['code', 'course', 'teacher', 'room', 'date_start', 'series', 'duration']
    raw_id_fields = ['teacher', 'assistant', 'course', 'academic_year', 'room', 'rmu']


@admin.register(LectureStudent)
class LectureStudentAdmin(admin.ModelAdmin):
    list_display = ['student', 'lecture', 'status']
    search_fields = ['student__person__fullname', 'lecture__name']
    raw_id_fields = ['student', 'lecture']


@admin.register(LectureScoreWeighting)
class LectureScoreWeigtingAdmin(admin.ModelAdmin):
    list_select_related = ['lecture']
    list_display = [
        'lecture', 'attendance', 'homework1', 'homework2', 'quis1', 'quis2',
        'mid_exam', 'final_exam', 'total']


@admin.register(LectureSchedule)
class LectureSceduleAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    search_fields = [
        'lecture__name', 'lecture__code', 'room__name',
        'lecture__teacher__person__fullname']
    list_display = ['lecture', 'session', 'room', 'date', 'time_start', 'time_end', 'type']
    raw_id_fields = ['lecture', 'room']
    radio_fields = {
        "type": admin.HORIZONTAL,
    }


class LectureStudentScoreInline(admin.TabularInline):
    extra = 0
    model = StudentScore


admin.site.register(LectureScore)