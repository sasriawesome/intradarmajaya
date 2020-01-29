from django.contrib import admin
from wagtailkit.sales.admin import OrderAdmin
from .models import LabOrder, LabOrderProduct


class LabOrderProductLine(admin.TabularInline):
    extra = 0
    model = LabOrderProduct
    raw_id_fields = ['product']


@admin.register(LabOrder)
class LabOrderAdmin(OrderAdmin):
    inlines = [LabOrderProductLine]
