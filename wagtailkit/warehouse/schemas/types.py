import graphene
from graphene_django import DjangoObjectType

from wagtailkit.warehouse.models import (
    WarehouseLocation,
    RequestOrder, AssetRequestItem, InventoryRequestItem,
    ProductTransfer, NewProduct, TransferCheckIn, TransferCheckOut,
    TransferScrapped, AssetTransferLine, InventoryTransferLine)


class WarehouseLocationType(DjangoObjectType):
    """ Product proxy as Warehouse Card Report """

    class Meta:
        model = WarehouseLocation


class RequestOrderType(DjangoObjectType):
    class Meta:
        model = RequestOrder


class AssetRequestItemType(DjangoObjectType):
    class Meta:
        model = AssetRequestItem


class InventoryRequestItemType(DjangoObjectType):
    class Meta:
        model = InventoryRequestItem

class NewProductRequestItemType(DjangoObjectType):
    class Meta:
        model = NewProduct

# TODO Next time
# class ProductTransferType(DjangoObjectType):
#     class Meta:
#         model = ProductTransfer
#
#
# class TransferCheckInType(DjangoObjectType):
#     class Meta:
#         model = TransferCheckIn
#
#
# class TransferCheckOutType(DjangoObjectType):
#     class Meta:
#         model = TransferCheckOut
#
#
# class TransferScrappedType(DjangoObjectType):
#     class Meta:
#         model = TransferScrapped
#
#
# class TransferItemType(DjangoObjectType):
#     class Meta:
#         model = TransferScrapped
