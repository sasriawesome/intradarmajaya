from django.contrib import admin
from wagtailkit.sales.models import Order, OrderProduct, OrderType


class OrderProductLine(admin.TabularInline):
    extra = 0
    min_num = 1
    model = OrderProduct
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductLine]
    date_hierarchy = 'date_created'
    search_fields = ['inner_id', 'customer']
    list_display = [
        'inner_id', 'customer', 'date_created',
        'total_order', 'discount', 'grand_total', 'status', ]
    list_select_related = ['customer']
    raw_id_fields = ['customer']


admin.site.register(OrderType)
