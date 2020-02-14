from django.contrib import admin
from django.utils import translation
from import_export.admin import ImportExportMixin
from wagtailkit.warehouse.models import StockAdjustment, AdjustedProduct

from wagtailkit.warehouse.resources import AdjustedProductResource

_ = translation.gettext_lazy


class AdjustedProductInline(admin.TabularInline):
    extra = 0
    model = AdjustedProduct


class AdjustedProductAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = AdjustedProductResource
    raw_id_fields = ['product']

class ProductStockAdjustmentAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['inner_id', 'title', 'effective_date', 'is_valid', 'is_reconciled', 'reconciled_by']
    inlines = [AdjustedProductInline]
