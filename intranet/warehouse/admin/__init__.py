from wagtail.contrib.modeladmin.options import modeladmin_register
from .warehouse import *
from .partners import *
from .products import *

modeladmin_register(ProductModelAdminGroup)
modeladmin_register(PartnerModelAdminGroup)
modeladmin_register(WarehouseAdminGroup)

