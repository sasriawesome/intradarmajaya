from django.utils.translation import gettext_lazy as _

from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, RichTextFieldPanel,
    TabbedInterface, ObjectList, FieldRowPanel)
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register, ModelAdminGroup
from wagtail.contrib.modeladmin.views import InspectView, CreateView

from wagtailautocomplete.edit_handlers import AutocompletePanel
from wagtailkit.importexport.admin import ImportExportModelAdminMixin
from wagtailkit.importexport.views import ImportExportIndexView
from wagtailkit.importexport.helpers import ImportExportAdminURLHelperMixin

from wagtailkit.sales.models import Order, OrderProduct


class OrderCreateView(CreateView):
    def get_instance(self):
        instance = super().get_instance()
        instance.creator = self.request.user
        return instance


class OrderInspectView(InspectView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = context['instance']
        context = {
            # 'warehouse_cards': warehouse_cards
        }
        context.update(**kwargs)
        return super().get_context_data(**context)


class OrderIndexView(ImportExportIndexView):
    pass


class OrderAdminURLHelper(ImportExportAdminURLHelperMixin):
    pass


class OrderModelAdmin(ImportExportModelAdminMixin, ModelAdmin):
    menu_icon = ' icon-fa-wpforms'
    menu_label = _('Order')
    model = Order
    # resource_class = OrderResource
    inspect_view_enabled = True
    index_view_class = OrderIndexView
    url_helper_class = OrderAdminURLHelper
    list_per_page = 20
    list_display = ['inner_id', 'customer', 'total_order', 'discount', 'grand_total', 'status']
    list_filter = ['date_created', 'order_type']
    search_fields = ['inner_id', 'customer__partner__name']

    info_panels = [
        MultiFieldPanel([
            FieldPanel('order_type'),
            FieldPanel('customer'),
            FieldPanel('customer_po'),
            FieldPanel('note'),
            FieldPanel('note'),
        ]),
    ]

    products_panels = [
        MultiFieldPanel([
            InlinePanel('order_products', panels=[
                AutocompletePanel('product'),
                FieldPanel('quantity')
            ]),
        ]),
    ]

    status_panels = [
        MultiFieldPanel([
            FieldPanel('total_order'),
            FieldPanel('discount_percentage'),
            FieldPanel('discount'),
            FieldPanel('grand_total'),
        ]),
    ]

    edit_handler = TabbedInterface([
        ObjectList(info_panels, heading=_('Info')),
        ObjectList(products_panels, heading=_('Products')),
        ObjectList(status_panels, heading=_('Status'))
    ])


class SalesAdminGroup(ModelAdminGroup):
    menu_icon = ' icon-fa-shopping-bag'
    menu_label = _('Sales')
    items = [OrderModelAdmin]


modeladmin_register(SalesAdminGroup)
