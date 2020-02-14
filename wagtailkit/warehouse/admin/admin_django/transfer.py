from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicParentModelAdmin
from wagtailkit.warehouse.models import (
    TransferCheckIn, TransferCheckOut, TransferScrapped, InventoryTransferLine, AssetTransferLine
)


class InventoryTranferInline(admin.TabularInline):
    extra = 0
    model = InventoryTransferLine


class AssetTransferInline(admin.TabularInline):
    extra = 0
    model = AssetTransferLine


class TransferMixin(admin.ModelAdmin):
    show_in_index = True
    inlines = [InventoryTranferInline, AssetTransferInline]
    date_hierarchy = 'date_created'
    list_filter = ['date_created']
    list_display = ['inner_id', 'creator', 'status']


class CheckInAdmin(TransferMixin, PolymorphicChildModelAdmin):
    pass


class CheckOutAdmin(TransferMixin, PolymorphicChildModelAdmin):
    pass


class ScrappedAdmin(TransferMixin, PolymorphicChildModelAdmin):
    pass


class TransferAdmin(TransferMixin, PolymorphicParentModelAdmin):
    child_models = [TransferCheckIn, TransferCheckOut, TransferScrapped]
