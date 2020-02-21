from .human_resource import *
from .warehouse import *
from .partners import *
from .products import *
from .discuss import *
from .academic import *
from .teachers import *
from .rooms import *
from .lectures import *

modeladmin_register(AcademicModelAdminGroup)
modeladmin_register(LectureModelAdminGroup)
modeladmin_register(CourseModelAdminGroup)
modeladmin_register(DiscussionsModelAdminGroup)
modeladmin_register(EmployeesAdminGroup)
modeladmin_register(TeacherModelAdminGroup)
modeladmin_register(StudentModelAdminGroup)
modeladmin_register(PartnerModelAdminGroup)
modeladmin_register(HumanResourceAdminGroup)

modeladmin_register(RoomModelAdminGroup)
modeladmin_register(ProductModelAdminGroup)
modeladmin_register(WarehouseAdminGroup)