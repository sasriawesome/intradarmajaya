from django.contrib import admin
from wagtailkit.academic.models import (
    CoursePreRequisite, CurriculumCourse, SchoolYear,
    ResourceManagementUnit, ProgramStudy, Curriculum, Course,
    CurriculumCourse)


@admin.register(SchoolYear)
class SchoolYearAdmin(admin.ModelAdmin):
    list_display = ['code', 'year', 'semester', 'date_start', 'date_end']


@admin.register(ResourceManagementUnit)
class ResourceManagementUnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'parent' ]


class CurriculumCourseInline(admin.TabularInline):
    extra = 0
    exclude = ['inner_id', 'reg_number', 'date_created']
    model = CurriculumCourse


@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    search_fields = ['name', 'prodi__name']
    exclude = ['inner_id', 'reg_number', 'date_created']
    inlines = [CurriculumCourseInline]
    list_display = ['name', 'sks_graduate', 'prodi', 'sks_mandatory', 'sks_choice']

    def get_queryset(self, request):
        return self.model.objects.get_detail_sks()

    def sks_mandatory(self, obj):
        return obj.sks_mandatory

    def sks_choice(self, obj):
        return obj.sks_choice


@admin.register(CurriculumCourse)
class CurriculumCourseAdmin(admin.ModelAdmin):
    show_in_index = False
    search_fields = ['course__name']
    exclude = ['inner_id', 'reg_number', 'date_created']
    list_select_related = ['course']
    list_display = ['inner_id', 'course', 'sks', 'sks_type']


@admin.register(ProgramStudy)
class ProgramStudyAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'rmu']


class CoursePreRequisiteInline(admin.TabularInline):
    extra = 0
    fk_name = 'course'
    model = CoursePreRequisite


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    search_fields = ['name']
    inlines = [CoursePreRequisiteInline]
    exclude = ['inner_id', 'reg_number']
    list_display = ['inner_id', 'name', 'rmu', 'equal_to', 'description', 'is_active']
