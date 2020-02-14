from import_export.resources import ModelResource
from import_export.widgets import ForeignKeyWidget
from import_export import fields

from wagtailkit.importexport.widgets import UUIDWidget, ExcelDateWidget

from .models import Inventory, Asset, Service, Bundle, ProductCategory, UnitOfMeasure

product_fields = [
    'id', 'inner_id', 'reg_number', 'name', 'barcode', 'description', 'category', 'unit_price',
    'minimum_stock', 'maximum_stock', 'unit_of_measure',
    'is_active', 'is_sparepart', 'can_be_sold', 'can_be_purchased', 'date_created'
]

service_fields = [
    'id', 'name', 'description', 'category', 'unit_price', 'unit_of_measure',
    'is_active', 'can_be_sold', 'can_be_purchased'
]

class ProductResourceMixin(ModelResource):
    id = fields.Field(attribute='id', column_name='id', widget=UUIDWidget())
    date_created = fields.Field(attribute='date_created', column_name='date_created',
                          widget=ExcelDateWidget(date_format='%d/%m/%Y %H:%M'))
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(ProductCategory, 'name'))
    unit_of_measure = fields.Field(
        column_name='unit_of_measure',
        attribute='unit_of_measure',
        widget=ForeignKeyWidget(UnitOfMeasure, 'name'))


class InventoryResource(ProductResourceMixin):
    class Meta:
        model = Inventory
        fields = product_fields


class AssetResource(ProductResourceMixin):
    class Meta:
        model = Asset
        fields = product_fields


class ServiceResource(ProductResourceMixin):
    class Meta:
        model = Service
        fields = service_fields


class BundleResource(ProductResourceMixin):
    class Meta:
        model = Bundle
        fields = product_fields
