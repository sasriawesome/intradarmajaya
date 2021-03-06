from django.contrib import admin

from wagtailkit.enrollments.models import Enrollment, EnrollmentItem, EnrollmentPlan


class EnrollmentItemLine(admin.TabularInline):
    extra = 0
    model = EnrollmentItem
    raw_id_fields = ['lecture']


@admin.register(EnrollmentPlan)
class EnrollmentAdmin(admin.ModelAdmin):
    pass

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    search_fields = ['student__sid', 'student__person__fullname']
    inlines = [EnrollmentItemLine]
    raw_id_fields = ['student']
    list_display = ['inner_id', 'student', 'date_created']