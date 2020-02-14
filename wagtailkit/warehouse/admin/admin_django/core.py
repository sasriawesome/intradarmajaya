from django.contrib import admin


class ProductStorageAdmin(admin.ModelAdmin):
    pass


class WarehouseLocationAdmin(admin.ModelAdmin):
    pass


class StockCardAdmin(admin.ModelAdmin):
    search_fields = ['product__inner_id', 'product__name', 'product__barcode']
    list_display = ['product', 'stock_on_hand', 'stock_on_delivery', 'stock_on_request', 'stock_scrapped']
