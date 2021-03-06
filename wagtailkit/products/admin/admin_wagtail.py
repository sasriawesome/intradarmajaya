from django.utils.translation import gettext_lazy as _

from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, RichTextFieldPanel,
    TabbedInterface, ObjectList)
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register, ModelAdminGroup
from wagtail.contrib.modeladmin.views import InspectView, CreateView

from wagtailkit.products.models import (
    Inventory, Asset, Service, Bundle,
    PaymentMethod, ProductCategory, DeliveryMethod, UnitOfMeasure)
from wagtailkit.products.resources import InventoryResource, AssetResource, ServiceResource, BundleResource
from wagtailkit.importexport.admin import ImportExportModelAdminMixin
from wagtailkit.importexport.views import ImportExportIndexView
from wagtailkit.importexport.helpers import ImportExportAdminURLHelperMixin

PRODUCT_PANEL = [
    MultiFieldPanel([
        ImageChooserPanel('picture'),
        FieldPanel('barcode'),
        FieldPanel('name'),
        FieldPanel('unit_of_measure'),
        FieldPanel('suppliers'),
        SnippetChooserPanel('category'),
        RichTextFieldPanel('description'),
    ])
]

SPEC_PANEL = [
    InlinePanel(
        'product_specifications',
        panels=[
            MultiFieldPanel([
                FieldPanel('feature'),
                FieldPanel('value'),
                FieldPanel('note'),
            ]),
        ]
    )
]

PART_PANEL = [
    InlinePanel(
        'spareparts',
        panels=[
            FieldPanel('sparepart'),
            FieldPanel('quantity'),
        ]
    )
]

OPTION_PANEL = [
    MultiFieldPanel([
        FieldPanel('unit_price'),
        FieldPanel('minimum_stock'),
        FieldPanel('maximum_stock')
    ], heading=_('Stock and Price')),
    MultiFieldPanel([
        FieldPanel('is_active'),
        FieldPanel('is_locked'),
        FieldPanel('is_sparepart'),
        FieldPanel('can_be_sold'),
        FieldPanel('can_be_purchased'),
    ], heading=_('Status')),
]


class ProductCreateView(CreateView):
    def get_instance(self):
        instance = super().get_instance()
        instance.creator = self.request.user
        return instance


class ProductInspectView(InspectView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = context['instance']
        # warehouse_cards = instance.warehouse_card(self.request)
        context = {
            # 'warehouse_cards': warehouse_cards
        }
        context.update(**kwargs)
        return super().get_context_data(**context)


class ProductIndexView(ImportExportIndexView):
    pass


class ProductAdminURLHelper(ImportExportAdminURLHelperMixin):
    pass


class ProductModelAdminBase(ImportExportModelAdminMixin, ModelAdmin):
    menu_icon = ' icon-fa-cube'
    list_display = ['inner_id', 'name', 'unit_price', 'minimum_stock', 'maximum_stock', 'is_active']
    list_filter = ['date_created', 'is_active', 'can_be_purchased']
    search_fields = ['inner_id', 'name', 'category__name']
    inspect_view_enabled = True
    index_view_class = ProductIndexView
    url_helper_class = ProductAdminURLHelper
    list_per_page = 20

    edit_handler = TabbedInterface([
        ObjectList(PRODUCT_PANEL, heading=_('Product')),
        ObjectList(SPEC_PANEL, heading=_('Specifications')),
        ObjectList(OPTION_PANEL, heading=_('Options')),
    ])


class InventoryModelAdmin(ProductModelAdminBase):
    model = Inventory
    resource_class = InventoryResource


class AssetModelAdmin(ProductModelAdminBase):
    model = Asset
    resource_class = AssetResource


class ServiceModelAdmin(ProductModelAdminBase):
    model = Service
    resource_class = ServiceResource


class BundleModelAdmin(ProductModelAdminBase):
    model = Bundle
    resource_class = BundleResource

    edit_handler = TabbedInterface([
        ObjectList(PRODUCT_PANEL, heading=_('Product')),
        ObjectList(SPEC_PANEL, heading=_('Specifications')),
        ObjectList(PART_PANEL, heading=_('Spareparts')),
        ObjectList(OPTION_PANEL, heading=_('Options')),
    ])


class PaymentMethodModelAdmin(ModelAdmin):
    menu_icon = 'fa-book'
    menu_label = _('Payments')
    model = PaymentMethod


class UnitOfMeasureModelAdmin(ModelAdmin):
    menu_icon = 'fa-exchange'
    menu_label = _('Units')
    model = UnitOfMeasure


class ProductCategoryModelAdmin(ModelAdmin):
    menu_icon = 'fa-tags'
    menu_label = _('Categories')
    model = ProductCategory


class DeliveryMethodModelAdmin(ModelAdmin):
    menu_icon = 'fa-truck'
    menu_label = _('Couriers')
    model = DeliveryMethod
