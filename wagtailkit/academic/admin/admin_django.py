from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from wagtailkit.academic.models import (
    CoursePreRequisite, AcademicYear, AcademicActivity, SchoolYear, CourseGroup, CourseType,
    ResourceManagementUnit, Faculty, ProgramStudy, Curriculum, Course,
    CurriculumCourse)


@admin.register(SchoolYear)
class SchoolYearAdmin(admin.ModelAdmin):
    list_display = ['code', 'year_start', 'year_end']


@admin.register(AcademicActivity)
class AcademicActivityAdmin(admin.ModelAdmin):
    search_fields = ['rmu__name', 'activity']
    list_display = ['activity', 'date_start', 'date_end', 'academic_year', 'rmu', 'status']
    raw_id_fields = ['rmu', 'academic_year']


class AcademicActivityInline(admin.TabularInline):
    extra = 0
    model = AcademicActivity


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ['code', 'school_year', 'semester', 'date_start', 'date_end']
    inlines = [AcademicActivityInline]


@admin.register(ResourceManagementUnit)
class ResourceManagementUnitAdmin(MPTTModelAdmin):
    list_display = ['name', 'code', 'parent']


class CurriculumCourseInline(admin.TabularInline):
    extra = 0
    model = CurriculumCourse
    raw_id_fields = ['course']


@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    search_fields = ['name', 'prodi__name']
    inlines = [CurriculumCourseInline]
    list_display = ['name', 'sks_graduate', 'prodi']
    raw_id_fields = ['prodi']


@admin.register(CurriculumCourse)
class CurriculumCourseAdmin(admin.ModelAdmin):
    search_fields = ['course__name']
    list_select_related = ['course']
    list_display = ['course_name', 'course_code', 'curricullum', 'semester_number',
                    'sks_meeting', 'sks_practice', 'sks_field_practice',
                    'sks_simulation', 'sks_total']
    raw_id_fields = ['course', 'curricullum']

    def course_name(self, obj):
        return obj.course_name

    def course_code(self, obj):
        return obj.course_code


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'code', 'alias']


@admin.register(ProgramStudy)
class ProgramStudyAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'code', 'alias', 'level', 'faculty', 'rmu']
    raw_id_fields = ['rmu', 'faculty']


@admin.register(CourseType)
class CourseType(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'code', 'alias']


@admin.register(CourseGroup)
class CourseGroup(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'code', 'alias']


class CoursePreRequisiteInline(admin.TabularInline):
    extra = 0
    fk_name = 'course'
    model = CoursePreRequisite


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    search_fields = ['name']
    inlines = [CoursePreRequisiteInline]
    list_display = ['code', 'name', 'rmu', 'equal_to', 'description', 'is_active']
