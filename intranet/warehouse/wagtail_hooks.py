from django.db import models
from django.contrib.auth import get_permission_codename
from wagtail.admin.navigation import get_site_for_user
from wagtail.admin.site_summary import SummaryItem
from wagtail.core import hooks

from wagtailkit.admin.helpers import PermissionHelper
from wagtailkit.products.models import Inventory, Asset
from wagtailkit.warehouse.models import (
    StockCard, RequestOrder, TransferCheckIn,
    TransferCheckOut, TransferScrapped)

ph_asset = PermissionHelper(Asset)
ph_inventory = PermissionHelper(Inventory)
ph_stock_card = PermissionHelper(StockCard)
ph_request_order = PermissionHelper(RequestOrder)
ph_checkin = PermissionHelper(TransferCheckIn)
ph_chekout = PermissionHelper(TransferCheckOut)
ph_scrapped = PermissionHelper(TransferScrapped)


class WarehouseWelcomePanel(SummaryItem):
    order = 51
    template = 'modeladmin/warehouse/admin_homepage_summary.html'

    def get_context(self):
        site_name = get_site_for_user(self.request.user)['site_name']
        user = self.request.user

        context = {
            'site_name': site_name,
        }

        if ph_inventory.user_has_any_permissions(user):
            inventory = Inventory.objects.get_summary()
            context.update({
                'inventory': inventory,
                'has_any_inventory_perm': ph_inventory.user_has_any_permissions(user),
                'can_create_inventory': ph_inventory.user_can_create(user),
                'can_edit_inventory': ph_inventory.user_has_specific_permission(user, 'change'),
                'can_view_inventory': ph_inventory.user_can_list(user),
            })

        if ph_asset.user_has_any_permissions(user):
            asset = Asset.objects.get_summary()
            context.update({
                'asset': asset,
                'has_any_asset_perm': ph_asset.user_has_any_permissions(user),
                'can_create_asset': ph_asset.user_can_create(user),
                'can_edit_asset': ph_asset.user_has_specific_permission(user, 'change'),
                'can_view_asset': ph_asset.user_can_list(user),
            })

        if ph_request_order.user_has_any_permissions(user):
            # show summary for position and childen
            # if user is member of Warehouse User or Warehouse Assistant
            user_can_view_other = ph_request_order.user_can('viewother', user)

            # Todo clean this up
            if user_can_view_other:
                request_order_summary = RequestOrder.objects.get_summary()
            else:
                request_order_summary = RequestOrder.objects.get_summary(
                    requester=user.person.employee.position, tree=True)

            context.update({
                'request_order': request_order_summary,
                'has_any_request_order_perm': ph_request_order.user_has_any_permissions(user),
                'can_create_request_order': ph_request_order.user_can_create(user),
                'can_edit_request_order': ph_request_order.user_has_specific_permission(user, 'change'),
                'can_view_request_order': ph_request_order.user_can_list(user),
            })

        if ph_checkin.user_has_any_permissions(user):
            check_in_summary = TransferCheckIn.objects.get_summary()
            context.update({
                'check_in': check_in_summary,
                'has_any_checkin_perm': ph_checkin.user_has_any_permissions(user),
                'can_create_checkin': ph_checkin.user_can_create(user),
                'can_edit_checkin': ph_checkin.user_has_specific_permission(user, 'change'),
                'can_view_checkin': ph_checkin.user_can_list(user),
            })

        if ph_chekout.user_has_any_permissions(user):
            check_out_summary = TransferCheckOut.objects.get_summary()
            context.update({
                'check_out': check_out_summary,
                'has_any_checkout_perm': ph_chekout.user_has_any_permissions(user),
                'can_create_checkout': ph_chekout.user_can_create(user),
                'can_edit_checkin': ph_chekout.user_has_specific_permission(user, 'change'),
                'can_view_checkout': ph_chekout.user_can_list(user),
            })

        if ph_chekout.user_has_any_permissions(user):
            scrap_summary = TransferScrapped.objects.get_summary()
            context.update({
                'scrap': scrap_summary,
                'has_any_checkout_perm': ph_scrapped.user_has_any_permissions(user),
                'can_create_checkout': ph_scrapped.user_can_create(user),
                'can_edit_checkin': ph_scrapped.user_has_specific_permission(user, 'change'),
                'can_view_checkout': ph_scrapped.user_can_list(user),
            })

        return context

    def is_shown(self):
        return ph_request_order.user_has_any_permissions(self.request.user)


@hooks.register('construct_homepage_panels')
def add_warehouse_welcome_panel(request, panels):
    welcome_panel = WarehouseWelcomePanel(request)
    if welcome_panel.is_shown():
        panels.append(WarehouseWelcomePanel(request))
