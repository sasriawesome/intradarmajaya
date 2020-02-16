from .human_resource import *
from .warehouse import *
from .partners import *
from .products import *
from .discuss import *

modeladmin_register(DiscussionsModelAdminGroup)
modeladmin_register(EmployeesAdminGroup)
modeladmin_register(PartnerModelAdminGroup)
modeladmin_register(HumanResourceAdminGroup)

modeladmin_register(ProductModelAdminGroup)
modeladmin_register(WarehouseAdminGroup)