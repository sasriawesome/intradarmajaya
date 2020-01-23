from django.contrib.admin.utils import quote, capfirst
from django.conf.urls import url
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _

from wagtail.contrib.modeladmin.options import ModelAdmin
from wagtail.contrib.modeladmin.helpers import PermissionHelper
from wagtail.admin.messages import messages
from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, FieldRowPanel, TabbedInterface,
    MultiFieldPanel, ObjectList)

from wagtailkit.admin.views import CreateView, InspectView
from wagtailkit.admin.helpers import ButtonHelper, PermissionHelper
from wagtailkit.printpdf.admin import PrintPDFModelAdminMixin
from wagtailkit.printpdf.helpers import PrintPDFButtonHelperMixin
from wagtailkit.importexport.admin import ImportExportModelAdminMixin
from wagtailkit.warehouse.models import StockCard, StockAdjustment

from wagtailautocomplete.edit_handlers import AutocompletePanel

class StockCardInspectView(InspectView):
    def get_context_data(self, **kwargs):
        context = {
            'histories': self.instance.get_history_items(self.request)
        }
        context.update(kwargs)
        return super().get_context_data(**context)


class StockCardModelAdmin(ModelAdmin):
    menu_icon = ' icon-fa-table'
    model = StockCard
    inspect_view_enabled = True
    list_per_page = 20
    inspect_view_class = StockCardInspectView
    search_fields = ['product__inner_id', 'product__name']
    list_display = ['product', 'stock_min', 'stock_max', 'stock_on_hand', 'stock_on_request',
                    'stock_on_delivery', 'stock_scrapped', 'stock', 'unit_price', 'total_price']


class AdjustmentButtonHelper(PrintPDFButtonHelperMixin, ButtonHelper):
    """ Stock adjusment button helper """

    buttons_exclude = []

    def get_buttons_for_obj(self, obj, exclude=None, classnames_add=None, classnames_exclude=None):
        exclude = [] if not exclude else exclude
        exclude = exclude + self.buttons_exclude
        classnames_add = [] if not classnames_add else classnames_add
        classnames_exclude = [] if not classnames_exclude else classnames_exclude
        ph = self.permission_helper
        usr = self.request.user
        pk = getattr(obj, self.opts.pk.attname)

        # add custom button
        btns = super().get_buttons_for_obj(obj, exclude, classnames_add, classnames_exclude)

        if 'validate' not in exclude and ph.user_can('validate', usr, obj) and not obj.is_valid:
            btns.append(self.create_custom_button('validate', pk, classnames_add, classnames_exclude))

        if 'reconcile' not in exclude and ph.user_can('reconcile', usr, obj) and obj.is_valid and not obj.is_reconciled:
            btns.append(self.create_custom_button('reconcile', pk, classnames_add, classnames_exclude))

        if 'add_all_product' not in exclude and ph.user_can('reconcile', usr,
                                                            obj) and not obj.is_valid and not obj.is_reconciled:
            btns.append(self.create_custom_button('add_all_product', pk, classnames_add, classnames_exclude))

        return btns


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
            'adjusted_products', label=_('Products'),
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
