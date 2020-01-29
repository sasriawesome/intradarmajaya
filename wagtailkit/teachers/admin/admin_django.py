from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtailkit.persons.admin.admin_django import PersonAdmin
from wagtailkit.teachers.models import Teacher, PersonAsTeacher


class TeacherFilter(admin.SimpleListFilter):
    """ Person filter by teacher """

    title = _('Teacher')
    parameter_name = 'teacher__isnull'

    def lookups(self, request, model_admin):
        return [
            (0, 'Ya'),
            (1, 'Tidak')
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            qs = queryset.filter(models.Q(teacher__isnull=bool(int(value))))
        else:
            qs = queryset.all()
        return qs


class TeacherInline(admin.TabularInline):
    model = Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    search_fields = ['person__fullname']
    list_display = ['name', 'fid', 'homebase', 'is_active']
    raw_id_fields = ('person',)

@admin.register(PersonAsTeacher)
class PersonAsTeacherAdmin(PersonAdmin):
    inlines = [TeacherInline]