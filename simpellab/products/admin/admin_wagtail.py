from django.utils.translation import gettext_lazy as _

from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, RichTextFieldPanel,
    TabbedInterface, ObjectList)
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register, ModelAdminGroup
from wagtail.contrib.modeladmin.views import InspectView, CreateView

from wagtailkit.importexport.admin import ImportExportModelAdminMixin
from wagtailkit.importexport.views import ImportExportIndexView
from wagtailkit.importexport.helpers import ImportExportAdminURLHelperMixin
from simpellab.products.models import LabService, Tarif, Fee
from simpellab.products.resources import LabServiceResource

PRODUCT_PANEL = [
    MultiFieldPanel([
        FieldPanel('name'),
        FieldPanel('service_type'),
        FieldPanel('unit_of_measure'),
        SnippetChooserPanel('category'),
        FieldPanel('unit_price'),
        RichTextFieldPanel('description'),
    ])
]

FEE_PANEL = [
    InlinePanel(
        'product_fees',
        panels=[
            FieldPanel('fee'),
            FieldPanel('price'),
        ]
    )
]

PARAMETER_PANEL = [
    InlinePanel(
        'product_parameters',
        panels=[
            MultiFieldPanel([
                FieldPanel('tarif'),
                FieldPanel('price'),
            ]),
        ]
    )
]

OPTION_PANEL = [
    MultiFieldPanel([
        FieldPanel('is_active'),
        FieldPanel('is_locked'),
    ]),
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
        context = {
            # 'warehouse_cards': warehouse_cards
        }
        context.update(**kwargs)
        return super().get_context_data(**context)


class ProductIndexView(ImportExportIndexView):
    pass


class ProductAdminURLHelper(ImportExportAdminURLHelperMixin):
    pass


class LabServiceModelAdmin(ImportExportModelAdminMixin, ModelAdmin):
    menu_icon = ' icon-fa-cube'
    menu_label = _('Service')
    model = LabService
    resource_class = LabServiceResource
    inspect_view_enabled = True
    index_view_class = ProductIndexView
    url_helper_class = ProductAdminURLHelper
    list_per_page = 20
    list_display = ['inner_id', 'name', 'total_fee', 'total_tarif', 'unit_price', 'is_active']
    list_filter = ['date_created', 'service_type']
    search_fields = ['inner_id', 'name', 'category__name']

    edit_handler = TabbedInterface([
        ObjectList(PRODUCT_PANEL, heading=_('Product')),
        ObjectList(FEE_PANEL, heading=_('Fees')),
        ObjectList(PARAMETER_PANEL, heading=_('Parameters')),
        ObjectList(OPTION_PANEL, heading=_('Options')),
    ])


class TarifModelAdmin(ModelAdmin):
    menu_icon = 'fa-list-alt'
    menu_label = _('Tarif')
    model = Tarif
    list_per_page = 20
    list_filter = ['service_type']
    search_fields = ['name']
    list_display = ['name', 'inner_id', 'price', 'date_effective']

    edit_handler = ObjectList([
        MultiFieldPanel([
            FieldPanel('service_type'),
            FieldPanel('name'),
            FieldPanel('price'),
            SnippetChooserPanel('category'),
            FieldPanel('date_effective'),
        ])
    ])


class FeeModelAdmin(ModelAdmin):
    menu_icon = 'fa-list-alt'
    menu_label = _('Fee')
    model = Fee
    list_per_page = 20
    search_fields = ['name']
    list_display = ['name', 'price', 'date_effective']

    edit_handler = ObjectList([
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('price'),
            FieldPanel('date_effective'),
        ])
    ])

from wagtailkit.products.admin.admin_wagtail import InventoryModelAdmin, AssetModelAdmin

class ProductAdminGroup(ModelAdminGroup):
    menu_icon = ' icon-fa-cubes'
    menu_label = _('Products')
    items = [InventoryModelAdmin, AssetModelAdmin, LabServiceModelAdmin, TarifModelAdmin, FeeModelAdmin]


modeladmin_register(ProductAdminGroup)
