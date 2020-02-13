from django.contrib.admin.utils import quote
from django.conf.urls import url
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _

from wagtail.contrib.modeladmin.options import ModelAdmin
from wagtail.contrib.modeladmin.helpers import PermissionHelper
from wagtail.admin.messages import messages
from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, FieldRowPanel, TabbedInterface,
    MultiFieldPanel, ObjectList)

from wagtailkit.autocompletes.edit_handlers import AutocompletePanel
from wagtailkit.admin.views import CreateView
from wagtailkit.admin.helpers import PermissionHelper
from wagtailkit.printpdf.admin import PrintPDFModelAdminMixin
from wagtailkit.warehouse.models import StockCard, StockAdjustment

from .helpers import AdjustmentButtonHelper
from .views import StockCardInspectView


class StockCardModelAdmin(ModelAdmin):
    menu_icon = ' icon-fa-table'
    model = StockCard
    inspect_view_enabled = True
    list_per_page = 20
    inspect_view_class = StockCardInspectView
    search_fields = ['product__inner_id', 'product__name']
    list_display = ['product', 'stock_min', 'stock_max', 'stock_on_hand', 'stock_on_request',
                    'stock_on_delivery', 'stock_scrapped', 'stock', 'unit_price', 'total_price']


class StockAdjustmentModelAdmin(PrintPDFModelAdminMixin, ModelAdmin):
    menu_icon = ' icon-fa-clipboard'
    menu_label = _('Adjustments')
    model = StockAdjustment
    inspect_view_enabled = True
    list_per_page = 20
    search_fields = ['title']
    list_filter = ['date_created', 'is_valid', 'is_reconciled']
    list_display = ['title', 'effective_date', 'is_valid', 'is_reconciled']
    button_helper_class = AdjustmentButtonHelper
    permission_helper_class = PermissionHelper
    create_view_class = CreateView

    adjustment_panel = [
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('description'),
            FieldPanel('effective_date')
        ])
    ]

    product_panel = [
        InlinePanel(
            'adjusted_products',
            panels=[
                AutocompletePanel('product'),
                FieldRowPanel([
                    FieldPanel('stock_on_hand'),
                    FieldPanel('new_stock_on_hand'),
                ]),
                FieldRowPanel([
                    FieldPanel('stock_scrapped'),
                    FieldPanel('new_stock_scrapped'),
                ])
            ]
        )
    ]

    edit_handler = TabbedInterface([
        ObjectList(adjustment_panel, heading=_('Information')),
        ObjectList(product_panel, heading=_('Products')),
    ])

    def get_admin_urls_for_registration(self):
        urls = super().get_admin_urls_for_registration()
        added_urls = (
            url(self.url_helper.get_action_url_pattern('validate'),
                self.validate_view, name=self.url_helper.get_action_url_name('validate')),
            url(self.url_helper.get_action_url_pattern('reconcile'),
                self.reconcile_view, name=self.url_helper.get_action_url_name('reconcile')),
            url(self.url_helper.get_action_url_pattern('add_all_product'),
                self.add_all_product_view, name=self.url_helper.get_action_url_name('add_all_product')),
            url(self.url_helper.get_action_url_pattern('print'),
                self.print_view, name=self.url_helper.get_action_url_name('print')),
        )
        return added_urls + urls

    def validate_view(self, request, instance_pk):
        # Set status
        codename = 'validate'
        instance = get_object_or_404(self.model, pk=instance_pk)
        perm_helper = self.permission_helper
        has_perm = perm_helper.user_can(codename, request.user, instance)
        try:
            if has_perm:
                getattr(instance, codename)()
                msg = _("Validation successfully.")
                messages.add_message(request, messages.SUCCESS, msg)
                return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))
        except Exception as err:
            messages.add_message(request, messages.ERROR, err)
            return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))

    def reconcile_view(self, request, instance_pk):
        # Set status
        codename = 'reconcile'
        instance = get_object_or_404(self.model, pk=instance_pk)
        perm_helper = self.permission_helper
        has_perm = perm_helper.user_can(codename, request.user, instance)
        try:
            if has_perm:
                getattr(instance, codename)(request)
                msg = _("Reconciliation successfully.")
                messages.add_message(request, messages.SUCCESS, msg)
                return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))
        except Exception as err:
            messages.add_message(request, messages.ERROR, err)
            return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))

    def add_all_product_view(self, request, instance_pk):
        # Set status
        codename = 'add_all_product'
        instance = get_object_or_404(self.model, pk=instance_pk)
        perm_helper = self.permission_helper
        has_perm = perm_helper.user_can('add', request.user, instance)
        try:
            if has_perm:
                getattr(instance, codename)(request)
                msg = _("All products added successfully.")
                messages.add_message(request, messages.SUCCESS, msg)
                return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))
        except Exception as err:
            messages.add_message(request, messages.ERROR, err)
            return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))

    def print_view(self, request, instance_pk):
        raise NotImplementedError
