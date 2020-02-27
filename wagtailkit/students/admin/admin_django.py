from django.contrib import admin

from wagtailkit.persons.admin.admin_django import PersonAdmin
from wagtailkit.students.models import Student, StudentPersonal, ConversionScore, StudentScore

class StudentInline(admin.TabularInline):
    model = Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    search_fields = ['person__fullname', 'sid']
    list_filter = ['status', 'year_of_force', 'registration']
    list_display = ['person', 'sid', 'rmu', 'year_of_force', 'registration', 'status']
    raw_id_fields = ['person', 'rmu']


@admin.register(StudentPersonal)
class StudentPersonalAdmin(PersonAdmin):
    inlines = [StudentInline]




@admin.register(StudentScore)
class StudentScoreAdmin(admin.ModelAdmin):
    search_fields = [
        'course__course__name', 'course__course__inner_id',
        'student__person__fullname', 'student__sid'
    ]
    raw_id_fields = ['student', 'course']
    list_display = ['student', 'course', 'numeric', 'alphabetic']

admin.site.register(ConversionScore)