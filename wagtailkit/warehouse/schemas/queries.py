import graphene

from wagtailkit.warehouse.models import (
    WarehouseLocation,
    RequestOrder, AssetRequestItem, InventoryRequestItem,
    ProductTransfer, NewProduct, TransferCheckIn, TransferCheckOut,
    TransferScrapped, AssetTransferLine, InventoryTransferLine)

from .types import (
    WarehouseLocationType, RequestOrderType, AssetRequestItemType, InventoryRequestItemType)


class WarehouseQuery:
    all_request_orders = graphene.List(RequestOrderType)

    def resolve_all_request_orders(self, info, **kwargs):
        return RequestOrder.objects.all()