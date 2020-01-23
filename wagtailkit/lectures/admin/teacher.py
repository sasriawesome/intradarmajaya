from django.core.exceptions import ValidationError
from django.db import models
from django.utils import translation, timezone
from django.contrib import admin, messages
from django.template.response import TemplateResponse
from django.shortcuts import reverse, redirect

from wa.admin import (
    ModelAdminBase, TabularInlineBase, ReadOnlyModelAdmin)
from zerp_person.admin import EducationHistoryInline
from zerp_lecture.models import Teacher

_ = translation.gettext_lazy


class TeacherInline(TabularInlineBase):
    model = Teacher
    exclude = ['created_by', 'modified_by', 'date_created', 'date_modified']


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


class PersonAsTeacherAdmin(ModelAdminBase):
    inlines = [TeacherInline]
    show_in_index = True
    exclude = ['reg_number', 'date_created']
    search_fields = ['person__name']
    list_display = ['fullname']
    fieldsets = (
        (_('Personal Info').upper(), {
            'fields': (
                'pro_pic', 'firstname', 'lastname')
        }
    ),)

    def is_user_label(self, obj):
        return bool(obj.is_user)

    def is_teacher_label(self, obj):
        return bool(obj.is_teacher)

    def is_active_teacher_label(self, obj):
        return False if not obj.is_teacher else obj.teacher.is_active

    is_user_label.boolean = True
    is_user_label.short_description = _("User")
    is_teacher_label.boolean = True
    is_teacher_label.short_description = _("Teacher")
    is_active_teacher_label.boolean = True
    is_active_teacher_label.short_description = _("Active")


    def get_queryset(self, request):
        if request.user.has_perms('zerp_academic.add_teacher'):
            return self.model.objects.get_persons()
        else:
            return super().get_queryset(request)

    def get_detail_view(self, request, object_id=None):
        try:
            profile_template = 'admin/profile.html'
            obj = self.model.objects.get(pk=object_id)
            context = {
                **self.admin_site.each_context(request),
                'instance': obj,
                'opts': self.model._meta,
                'title': '{}'.format(self.model._meta.verbose_name),
            }
            return TemplateResponse(request, profile_template, context=context)
        except ValidationError as err:
            self.message_user(request, err[0], level=messages.ERROR)
            return redirect(
                reverse(
                    'zerpadmin:%s_%s_changelist' % self.get_model_info()))
        except self.model.DoesNotExist as err:
            self.message_user(request, err, level=messages.ERROR)
            return redirect(
                reverse(
                    'zerpadmin:%s_%s_changelist' % self.get_model_info()))


class TeacherAdmin(ReadOnlyModelAdmin):
    show_in_index = False
    search_fields = ['person__firstname', 'person__lastname']
    list_display = ['name', 'lid', 'homebase', 'is_active']


class TeacherCourseAdmin(ModelAdminBase):
    search_fields = [
        'teacher__person__firstname', 'teacher__person__lastname']
    list_display = [
        'teacher', 'assistant', 'curriculum_course', 'school_year',
        'semester', 'is_active']
