from django.utils import translation
from django.db import models
from django.contrib import admin

from zerp_core.admin import ModelAdminBase, TabularInlineBase
from zerp_person.admin import EducationHistoryInline
from zerp_lecture.models import Student, Student, LectureStudent

_ = translation.gettext_lazy


class StudentInline(TabularInlineBase):
    model = Student
    exclude = ['created_by']


class StudentFilter(admin.SimpleListFilter):
    """ Person filter by student """

    title = _('Student')
    parameter_name = 'student__isnull'

    def lookups(self, request, model_admin):
        return [
            (0, _('Yes')),
            (1, _('No'))
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            qs = queryset.filter(models.Q(student__isnull=bool(int(value))))
        else:
            qs = queryset.all()
        return qs


class PersonAsStudentAdmin(ModelAdminBase):
    inlines = [StudentInline]
    show_in_index = True
    exclude = ['reg_number', 'date_created']
    search_fields = ['person__name']
    list_display = ['fullname']
    fieldsets = (
        (_('Personal Info'), {
            'fields': (
                'pro_pic', 'firstname', 'lastname')
        }
    ),)

    def is_student_label(self, obj):
        return bool(obj.is_student)

    def is_user_label(self, obj):
        return bool(obj.is_user)

    def is_active_student_label(self, obj):
        return False if not obj.is_student else obj.student.is_active

    is_student_label.boolean = True
    is_student_label.short_description = _("Student")
    is_user_label.boolean = True
    is_user_label.short_description = _("User")
    is_active_student_label.boolean = True
    is_active_student_label.short_description = _("Active")

    def get_queryset(self, request):
        if request.user.has_perms('zerp_academic.add_student'):
            return self.model.objects.get_persons()
        else:
            return super().get_queryset(request)

class LectureStudentInline(TabularInlineBase):
    extra = 0
    model = LectureStudent


class StudentEnrollmentAdmin(ModelAdminBase):
    show_in_index = True
    exclude = ['inner_id', 'reg_number', 'date_created']
    inlines = [LectureStudentInline]
