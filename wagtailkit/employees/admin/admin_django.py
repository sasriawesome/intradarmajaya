from django.contrib import admin
from django.utils import translation, timezone
from mptt.admin import MPTTModelAdmin

from wagtailkit.employees.models import Department, Chair, Chairman, Employee, PersonAsEmployee

_ = translation.gettext_lazy


@admin.register(Department)
class DepartmentAdmin(MPTTModelAdmin):
    show_in_index = True
    exclude = ['slug', 'metafield', 'creator']
    search_fields = ['name']
    list_display = ['name', 'level']


@admin.register(Chair)
class ChairAdmin(MPTTModelAdmin):
    show_in_index = True
    search_fields = ['department__name']
    exclude = ['slug', 'metafield']
    list_select_related = ['department']
    list_display = ['position', 'level', 'department']


@admin.register(Chairman)
class ChairmanAdmin(admin.ModelAdmin):
    exclude = ['metafield']
    list_display = ['verbose_name', 'is_active']
    list_select_related = ['employee', 'chair']

    def department(self, obj):
        return obj.chair.department


class EmployeeInline(admin.TabularInline):
    min_num = 1
    model = Employee
    exclude = ['metafield', 'creator', 'date_created']


@admin.register(PersonAsEmployee)
class PersonAsEmployeeAdmin(admin.ModelAdmin):
    show_in_index = True
    inlines = [EmployeeInline]
    exclude = ['reg_number', 'date_created', 'creator']
    search_fields = ['person__name']
    list_display = ['fullname']

    def is_user_label(self, obj):
        return bool(obj.is_user)

    def is_employee_label(self, obj):
        return obj.is_employee

    def is_active_employee_label(self, obj):
        return False if not obj.is_employee else obj.employee.is_active

    is_user_label.boolean = True
    is_employee_label.boolean = True
    is_active_employee_label.boolean = True

    is_user_label.short_description = _("User")
    is_employee_label.short_description = _("Employee")
    is_active_employee_label.short_description = _("Active")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        parent = form.instance
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            if not instance.creator:
                instance.creator = request.user
            instance.save()
        formset.save_m2m()
        parent.save()


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    show_in_index = True
    search_fields = ['eid', ]
    exclude = ['creator', 'date_created', 'metafield']
    list_display = ['eid', 'person', 'department', 'is_active_label', 'is_user']
    list_select_related = ['person', 'department']

    def is_user(self, obj):
        return obj.person.is_user

    def is_active_label(self, obj):
        return obj.is_active

    is_user.boolean = True
    is_active_label.boolean = True
    is_active_label.short_description = _("Active")


class EmploymentAdmin(admin.ModelAdmin):
    exclude = ['slug']
