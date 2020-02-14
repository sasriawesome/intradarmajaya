from django.contrib import admin

from wagtailkit.warehouse.models import InventoryRequestItem, AssetRequestItem, NewProduct


class NewProductAdmin(admin.TabularInline):
    extra = 0
    model = NewProduct


class AssetRequestItemInline(admin.TabularInline):
    extra = 0
    model = AssetRequestItem


class InventoryRequestItemInline(admin.TabularInline):
    extra = 0
    model = InventoryRequestItem


class RequestOrderAdmin(admin.ModelAdmin):
    inlines = [InventoryRequestItemInline, AssetRequestItemInline]
    date_hierarchy = 'date_created'
    list_filter = ['date_created', 'deadline', 'status']
    list_display = ['inner_id', 'requester', 'deliver_to', 'department', 'date_created', 'creator', 'status']
