from import_export.resources import ModelResource
from import_export import widgets, fields
from import_export.fields import Field

from wagtailkit.importexport.widgets import ExcelDateWidget, UUIDWidget
from .models import Employee


class EmployeeResource(ModelResource):
    class Meta:
        model = Employee
        fields = (
            'id', 'inner_id', 'reg_number','phone1', 'phone2', 'email', 'reg_number',
            'title', 'front_title', 'fullname', 'back_title', 'gender',
            'religion', 'nation', 'place_of_birth', 'date_of_birth', 'last_education_level',
            'last_education_institution', 'last_education_name', 'year_graduate', 'date_created',
            'is_employee_applicant')

    id = Field(attribute='id', column_name='id', widget=UUIDWidget())
    eid = Field(attribute='eid', column_name='eid', readonly=True, widget=widgets.CharWidget())