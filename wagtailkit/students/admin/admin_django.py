from django.contrib import admin

from wagtailkit.persons.admin.admin_django import PersonAdmin
from wagtailkit.students.models import Student, PersonAsStudent


class StudentInline(admin.TabularInline):
    model = Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    search_fields = ['person__fullname', 'sid']
    list_filter = ['program_study']
    list_display = ['person', 'sid', 'program_study']
    raw_id_fields = ['person', 'program_study']


@admin.register(PersonAsStudent)
class PersonAsStudentAdmin(PersonAdmin):
    inlines = [StudentInline]

