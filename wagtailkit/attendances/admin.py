from django.contrib import admin

from .models import TeacherAttendance, StudentAttendance, LectureAttendance


@admin.register(TeacherAttendance)
class TeacherAttendanceAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'schedule', 'note']


@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'schedule', 'status', 'note']


class StudentAttendanceInline(admin.TabularInline):
    extra = 0
    model = StudentAttendance


class TeacherAttendanceInline(admin.TabularInline):
    extra = 0
    max_num = 2
    model = TeacherAttendance


@admin.register(LectureAttendance)
class LectureSceduleAdmin(admin.ModelAdmin):
    save_as_continue = True
    save_as = True
    date_hierarchy = 'date'
    inlines = [TeacherAttendanceInline, StudentAttendanceInline]
    search_fields = [
        'lecture__name', 'lecture__code', 'room__name',
        'lecture__teacher__person__fullname']
    list_display = ['lecture', 'session', 'room', 'date', 'time_start', 'time_end', 'type']
    raw_id_fields = ['lecture', 'room']
    radio_fields = {"type": admin.HORIZONTAL}
