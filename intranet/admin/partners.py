from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdminGroup

from wagtailkit.partners.admin import (
    PartnerPersonalModelAdmin,
    PartnerModelAdmin,
    CustomerModelAdmin,
    SupplierModelAdmin
)

class PartnerModelAdminGroup(ModelAdminGroup):
    menu_label = _('Partners')
    menu_icon = 'fa-user-circle'
    items = [
        PartnerModelAdmin,
        PartnerPersonalModelAdmin,
        CustomerModelAdmin,
        SupplierModelAdmin
    ]