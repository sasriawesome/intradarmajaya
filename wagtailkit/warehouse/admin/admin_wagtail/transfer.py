from django.contrib.admin.utils import quote
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _

from wagtail.admin.messages import messages
from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, TabbedInterface, ObjectList)
from wagtail.contrib.modeladmin.options import ModelAdmin

from wagtailkit.autocompletes.edit_handlers import AutocompletePanel
from wagtailkit.printpdf.admin import PrintPDFModelAdminMixin
from wagtailkit.warehouse.models import (
    TransferCheckIn, TransferCheckOut, TransferScrapped, WarehouseLocation)
from wagtailkit.admin.admin import StatusModelAdminMixin
from wagtailkit.admin.views import CreateView, EditView

from .helpers import ProductTransferButtonHelper, ProductTransferPermissionHelper


class ProductTransferModelAdminBase(PrintPDFModelAdminMixin, StatusModelAdminMixin):
    list_filter = ['date_created', 'status']
    inspect_view_enabled = True
    button_helper_class = ProductTransferButtonHelper
    permission_helper_class = ProductTransferPermissionHelper
    create_view_class = CreateView
    edit_view_class = EditView
    list_per_page = 20

    order_panel = NotImplemented

    inventory_panels = [
        InlinePanel(
            'inventory_transfers',
            panels=[
                AutocompletePanel('product'),
                FieldPanel('quantity'),
            ]
        ),
    ]

    asset_panels = [
        InlinePanel(
            'asset_transfers',
            panels=[
                AutocompletePanel('product'),
                FieldPanel('quantity'),
            ]
        ),
    ]

    def get_edit_handler(self, instance, request):
        edit_handler = TabbedInterface([
            ObjectList(self.order_panel, heading=_('Information')),
            ObjectList(self.inventory_panels, heading=_('Inventory')),
            ObjectList(self.asset_panels, heading=_('Asset')),
        ])
        return edit_handler


class TransferCheckInModelAdmin(ProductTransferModelAdminBase):
    model = TransferCheckIn
    menu_icon = 'collapse-down'
    menu_label = _('Check In')
    detail_document_title = _('Check In Form')
    search_fields = ('inner_id', 'sender', 'reference')
    list_display = ['inner_id', 'sender', 'reference', 'date_created', 'status']

    order_panel = [
        MultiFieldPanel([
            FieldPanel('sender'),
            FieldPanel('reference'),
            FieldPanel('department'),
            FieldPanel('received_date'),
            FieldPanel('title'),
            FieldPanel('description'),
        ]),
    ]

    def complete_view(self, request, instance_pk):
        # Set status
        instance = get_object_or_404(self.model, pk=instance_pk)
        codename = 'complete'
        perm_helper = self.permission_helper
        has_perm = perm_helper.user_can(codename, request.user, instance)
        try:
            if has_perm:
                instance.complete_and_sync_stock(request)
                return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))
            raise PermissionError
        except Exception as err:
            messages.add_message(request, messages.ERROR, err)
            return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))


class TransferCheckOutModelAdmin(ProductTransferModelAdminBase):
    model = TransferCheckOut
    menu_icon = 'collapse-up'
    menu_label = _('Check Out')
    detail_document_title = _('Check Out Form')
    list_display = ['inner_id', 'request_order', 'requester', 'department', 'date_created', 'status']

    order_panel = [
        MultiFieldPanel([
            # FieldPanel('status'),
            AutocompletePanel('request_order'),
            # FieldPanel('requester'),
            # FieldPanel('department'),
            # FieldPanel('deliver_to'),
            FieldPanel('delivered_date'),
            FieldPanel('title'),
            FieldPanel('description'),
        ]),
    ]

    def validate_view(self, request, instance_pk):
        # Set status
        codename = 'validate'
        instance = get_object_or_404(self.model, pk=instance_pk)
        perm_helper = self.permission_helper
        has_perm = perm_helper.user_can(codename, request.user, instance)
        try:
            if instance.request_order.is_valid:
                messages.add_message(request, messages.ERROR, _('Waiting for request order approval'))
                return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))
            if has_perm:
                instance.validate_and_process_reference(request)
                messages.add_message(
                    request, messages.SUCCESS, _('Product checkout validated, and request order processed'))
                return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))
            raise PermissionError
        except Exception as err:
            messages.add_message(request, messages.ERROR, err)
            return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))

    def complete_view(self, request, instance_pk):
        # Set status
        instance = get_object_or_404(self.model, pk=instance_pk)
        codename = 'complete'
        perm_helper = self.permission_helper
        has_perm = perm_helper.user_can(codename, request.user, instance)
        try:
            if has_perm:
                instance.complete_and_sync_stock(request)
                return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))
            raise PermissionError
        except Exception as err:
            messages.add_message(request, messages.ERROR, err)
            return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))


class TransferScrappedModelAdmin(ProductTransferModelAdminBase):
    model = TransferScrapped
    menu_icon = 'bin'
    menu_label = _('Scrapped')
    search_fields = ['inner_id', 'reference']
    list_filter = ['date_created', 'status']
    detail_document_title = _('Product Scrapped Report')
    list_display = ['inner_id', 'reference', 'location', 'date_created', 'status']

    order_panel = [
        MultiFieldPanel([
            # FieldPanel('status'),
            FieldPanel('remover'),
            FieldPanel('reference'),
            FieldPanel('location'),
            FieldPanel('scrapped_date'),
            FieldPanel('title'),
            FieldPanel('description'),
        ]),
    ]

    def validate_view(self, request, instance_pk):
        # Set status
        codename = 'validate'
        instance = get_object_or_404(self.model, pk=instance_pk)
        perm_helper = self.permission_helper
        has_perm = perm_helper.user_can(codename, request.user, instance)
        try:
            if has_perm:
                instance.validate_and_process_reference(request)
                return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))
            raise PermissionError
        except Exception as err:
            messages.add_message(request, messages.ERROR, err)
            return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))

    def complete_view(self, request, instance_pk):
        # Set status
        instance = get_object_or_404(self.model, pk=instance_pk)
        codename = 'complete'
        perm_helper = self.permission_helper
        has_perm = perm_helper.user_can(codename, request.user, instance)
        try:
            if has_perm:
                instance.complete_and_sync_stock(request)
                return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))
            raise PermissionError
        except Exception as err:
            messages.add_message(request, messages.ERROR, err)
            return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))


class WarehouseLocationModelAdmin(ModelAdmin):
    model = WarehouseLocation
    menu_label = _('Locations')
    menu_icon = 'fa-podcast'

    edit_handler = ObjectList([
        MultiFieldPanel([
            FieldPanel('parent'),
            FieldPanel('code'),
            FieldPanel('name'),
            FieldPanel('loc_type'),
        ])
    ])
