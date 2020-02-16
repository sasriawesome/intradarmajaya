from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdminGroup

from wagtailkit.products.admin import (
    InventoryModelAdmin,
    AssetModelAdmin,
    ServiceModelAdmin,
    ProductCategoryModelAdmin,
    UnitOfMeasureModelAdmin,
    DeliveryMethodModelAdmin,
    PaymentMethodModelAdmin
)


class ProductModelAdminGroup(ModelAdminGroup):
    menu_icon = 'fa-cubes'
    menu_label = _('Products')
    items = [
        InventoryModelAdmin,
        AssetModelAdmin,
        ServiceModelAdmin,
        ProductCategoryModelAdmin,
        UnitOfMeasureModelAdmin,
        DeliveryMethodModelAdmin,
        PaymentMethodModelAdmin
    ]
