from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdminGroup

from wagtailkit.warehouse.admin import (
    StockCardModelAdmin,
    StockAdjustmentModelAdmin,
    RequestOrderModelAdmin,
    TransferCheckInModelAdmin,
    TransferCheckOutModelAdmin,
    TransferScrappedModelAdmin,
    WarehouseLocationModelAdmin
)

class WarehouseAdminGroup(ModelAdminGroup):
    menu_icon = ' icon-fa-institution'
    menu_label = _('Warehouse')
    items = (
        RequestOrderModelAdmin,
        TransferCheckInModelAdmin,
        TransferCheckOutModelAdmin,
        TransferScrappedModelAdmin,
        StockCardModelAdmin,
        StockAdjustmentModelAdmin,
        WarehouseLocationModelAdmin,
    )