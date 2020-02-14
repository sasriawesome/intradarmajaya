from django.contrib import admin

from wagtailkit.persons.admin.admin_django import PersonAdmin
from wagtailkit.students.models import Student, StudentPersonal
from wagtailkit.academic.admin.admin_wagtail import ProgramStudyFilter

class StudentInline(admin.TabularInline):
    model = Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    search_fields = ['person__fullname', 'sid']
    list_filter = ['status', ProgramStudyFilter, 'year_of_force', 'registration']
    list_display = ['person', 'sid', 'rmu', 'year_of_force', 'registration', 'status']
    raw_id_fields = ['person', 'rmu']


@admin.register(StudentPersonal)
class StudentPersonalAdmin(PersonAdmin):
    inlines = [StudentInline]