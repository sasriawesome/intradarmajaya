from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdminGroup, modeladmin_register

from .adjustment import StockCardModelAdmin, StockAdjustmentModelAdmin
from .request import RequestOrderModelAdmin
from .transfer import (
    TransferCheckInModelAdmin,
    TransferCheckOutModelAdmin,
    TransferScrappedModelAdmin
)


class WarehouseAdminGroup(ModelAdminGroup):
    menu_icon = ' icon-fa-institution'
    menu_label = _('Warehouse')
    items = (
        StockCardModelAdmin,
        StockAdjustmentModelAdmin,
        RequestOrderModelAdmin,
        TransferCheckInModelAdmin,
        TransferCheckOutModelAdmin,
        TransferScrappedModelAdmin
    )


modeladmin_register(WarehouseAdminGroup)
