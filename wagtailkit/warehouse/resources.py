from import_export.resources import ModelResource
from import_export.widgets import ForeignKeyWidget
from import_export import fields

from wagtailkit.importexport.widgets import UUIDWidget

from wagtailkit.products.models import Product
from .models import AdjustedProduct, StockAdjustment



class AdjustedProductResource(ModelResource):
    class Meta:
        model = AdjustedProduct
        fields = [
            'sort_order',
            'id',
            'date_created',
            'date_modified',
            'stock_adjustment',
            'product',
            'stock_on_hand',
            'stock_scrapped',
            'new_stock_on_hand',
            'new_stock_scrapped'
        ]
    id = fields.Field(attribute='id', column_name='id', widget=UUIDWidget())
    stock_adjustment = fields.Field(
        column_name='stock_adjustment',
        attribute='stock_adjustment',
        widget=ForeignKeyWidget(StockAdjustment, 'inner_id'))
    product = fields.Field(
        column_name='product',
        attribute='product',
        widget=ForeignKeyWidget(Product, 'inner_id'))
