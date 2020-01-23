from django.contrib import admin

from import_export.admin import ImportExportMixin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from wagtailkit.products.models import (
    PaymentMethod, DeliveryMethod, ProductCategory, UnitOfMeasure,
    Product, Inventory, Asset, Service, Bundle, Specification, Sparepart)


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    pass


@admin.register(DeliveryMethod)
class DeliveryMethodAdmin(admin.ModelAdmin):
    pass


@admin.register(UnitOfMeasure)
class UnitOfMeasureAdmin(ImportExportMixin, admin.ModelAdmin):
    show_in_index = True
    search_fields = ['name']


@admin.register(ProductCategory)
class ProductCategoryAdmin(ImportExportMixin, admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['inner_id', 'name', 'parent', 'tree_id']


class ProductSpecificationInline(admin.TabularInline):
    extra = 0
    model = Specification


class SparepartInline(admin.TabularInline):
    extra = 0
    model = Sparepart
    fk_name = 'product'


class ProductMixin(admin.ModelAdmin):
    inlines = [ProductSpecificationInline]
    ordering = ['-date_created']
    search_fields = ['inner_id', 'name']
    date_hierarchy = 'date_created'
    list_display = ['inner_id', 'name', 'barcode']


@admin.register(Product)
class ProductAdmin(ProductMixin, ImportExportMixin, PolymorphicParentModelAdmin):
    search_fields = ['inner_id', 'name', 'barcode']
    child_models = [Inventory, Asset, Service, Bundle]


@admin.register(Inventory)
class InventoryAdmin(ImportExportMixin, PolymorphicChildModelAdmin, ProductMixin):
    show_in_index = True
    base_model = Product


@admin.register(Asset)
class ProductAdmin(ImportExportMixin, PolymorphicChildModelAdmin, ProductMixin):
    show_in_index = True
    base_model = Product


@admin.register(Service)
class ProductAdmin(ImportExportMixin, PolymorphicChildModelAdmin, ProductMixin):
    show_in_index = True
    base_model = Product


@admin.register(Bundle)
class BundleAdmin(ImportExportMixin, PolymorphicChildModelAdmin, ProductMixin):
    show_in_index = True
    base_model = Product
    inlines = [ProductSpecificationInline, SparepartInline]
