from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from wagtailkit.persons.models import (
    Person, FormalEducation, NonFormalEducation, Working, Volunteer,
    Skill, Publication, Family, Award, PersonSettings
)

from wagtailkit.persons.resources import PersonResource


@admin.register(PersonSettings)
class PersonSettingAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        obj.site = request.site
        super().save_model(request, obj, form, change)

class EducationLevelAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['slug', 'name', 'description']


class FormalEducationInline(admin.TabularInline):
    extra = 0
    model = FormalEducation


class NonFormalEducationInline(admin.TabularInline):
    extra = 0
    model = NonFormalEducation


class WorkingInline(admin.TabularInline):
    extra = 0
    model = Working


class OrganizationInline(admin.TabularInline):
    extra = 0
    model = Volunteer


class SkillsInline(admin.TabularInline):
    extra = 0
    model = Skill


class AwardsInline(admin.TabularInline):
    extra = 0
    model = Award


class PublicationsInline(admin.TabularInline):
    extra = 0
    model = Publication


class FamilyInline(admin.TabularInline):
    extra = 0
    model = Family


class PersonAdmin(ImportExportModelAdmin):
    list_display = ['inner_id', 'fullname', 'date_of_birth']
    search_fields = ['fullname']
    resource_class = PersonResource
    inlines = [
        SkillsInline,
        AwardsInline,
        FormalEducationInline,
        NonFormalEducationInline,
        WorkingInline,
        OrganizationInline,
        PublicationsInline,
        FamilyInline
    ]


class FormalEducationAdmin(ImportExportModelAdmin):
    list_display = ['person', 'level']


class NonFormalEducationAdmin(ImportExportModelAdmin):
    list_display = ['person']


class WorkingAdmin(ImportExportModelAdmin):
    list_display = ['person', 'institution_name']


class VolunteerAdmin(ImportExportModelAdmin):
    list_display = ['person', 'organization']


class SkillsAdmin(ImportExportModelAdmin):
    list_display = ['person', 'name']


class AwardsAdmin(ImportExportModelAdmin):
    list_display = ['person', 'name']


class PublicationAadmin(ImportExportModelAdmin):
    list_display = ['person', 'title']


class FamilyAdmin(ImportExportModelAdmin):
    list_display = ['person', 'name']


admin.site.register(Person, PersonAdmin)
admin.site.register(FormalEducation, FormalEducationAdmin)
admin.site.register(NonFormalEducation, NonFormalEducationAdmin)
admin.site.register(Working, WorkingAdmin)
admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Skill, SkillsAdmin)
admin.site.register(Award, AwardsAdmin)
admin.site.register(Publication, PublicationAadmin)
admin.site.register(Family, FamilyAdmin)
