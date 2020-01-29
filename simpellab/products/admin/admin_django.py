from django.contrib import admin

from import_export.admin import ImportExportMixin

from wagtailkit.products.models import Product
from simpellab.products.models import (
    Tarif, Fee, ExtraFee, LabService, Parameter)
from simpellab.products.forms import (
    LabServiceForm
)


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    search_fields = ['name', 'inner_id']
    list_display = ['inner_id', 'name', 'price']

@admin.register(Tarif)
class TarifAdmin(admin.ModelAdmin):
    search_fields = ['name', 'inner_id']
    list_display = ['inner_id', 'name', 'price', 'category', 'service_type']
    list_filter = ['service_type']
    raw_id_fields = ['category']


class ProductMixin(admin.ModelAdmin):
    ordering = ['-date_created']
    search_fields = ['inner_id', 'name']
    list_filter = ['service_type']
    list_display = ['inner_id', 'name', 'total_fee', 'total_tarif', 'unit_price']
    raw_id_fields = ['category', 'picture', 'unit_of_measure']


class ExtraFeeLine(admin.TabularInline):
    extra = 0
    model = ExtraFee
    raw_id_fields = ('fee',)


class ParameterLine(admin.TabularInline):
    extra = 0
    model = Parameter
    raw_id_fields = ('tarif',)


@admin.register(LabService)
class ProductLabAdmin(ImportExportMixin, ProductMixin):
    save_as = True
    inlines = [ExtraFeeLine, ParameterLine]
    form = LabServiceForm
    base_model = Product
