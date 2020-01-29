from import_export.resources import ModelResource
from import_export.widgets import ForeignKeyWidget
from import_export import fields

from wagtailkit.importexport.widgets import UUIDWidget

from wagtailkit.products.models import UnitOfMeasure
from .models import LabService, ProductCategory

service_fields = [
    'id', 'name', 'description', 'category', 'unit_price', 'unit_of_measure',
    'is_active', 'service_type'
]

class ProductResourceMixin(ModelResource):
    id = fields.Field(attribute='id', column_name='id', widget=UUIDWidget())
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(ProductCategory, 'name'))
    unit_of_measure = fields.Field(
        column_name='unit_of_measure',
        attribute='unit_of_measure',
        widget=ForeignKeyWidget(UnitOfMeasure, 'name'))

class LabServiceResource(ProductResourceMixin):
    class Meta:
        model = LabService
        fields = service_fields
