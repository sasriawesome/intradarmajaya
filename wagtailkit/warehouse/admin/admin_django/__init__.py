from django.contrib import admin
from wagtailkit.warehouse.models import (
    RequestOrder, WarehouseLocation, StockCard, ProductStorage,
    TransferCheckIn, TransferCheckOut, TransferScrapped,
    ProductTransfer, StockAdjustment, AdjustedProduct
)

from .core import WarehouseLocationAdmin, StockCardAdmin, ProductStorageAdmin
from .stock import ProductStockAdjustmentAdmin, AdjustedProductAdmin
from .request import RequestOrderAdmin
from .transfer import TransferAdmin, CheckOutAdmin, CheckInAdmin, ScrappedAdmin

admin.site.register(WarehouseLocation, WarehouseLocationAdmin)
admin.site.register(RequestOrder, RequestOrderAdmin)
admin.site.register(StockCard, StockCardAdmin)
admin.site.register(ProductStorage, ProductStorageAdmin)
admin.site.register(TransferCheckOut, CheckOutAdmin)
admin.site.register(TransferCheckIn, CheckInAdmin)
admin.site.register(TransferScrapped, ScrappedAdmin)
admin.site.register(ProductTransfer, TransferAdmin)
admin.site.register(StockAdjustment, ProductStockAdjustmentAdmin)
admin.site.register(AdjustedProduct, AdjustedProductAdmin)