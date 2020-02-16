from import_export.resources import ModelResource
from import_export import widgets, fields
from import_export.fields import Field

from wagtailkit.importexport.widgets import ExcelDateWidget, UUIDWidget
from .models import Person


class PersonResource(ModelResource):
    class Meta:
        model = Person
        fields = (
            'id', 'inner_id', 'phone1', 'phone2', 'email', 'reg_number',
            'title', 'fullname', 'front_title', 'back_title', 'gender',
            'religion', 'nation', 'date_of_birth', 'place_of_birth')

    id = Field(attribute='id', column_name='id', widget=UUIDWidget())
    inner_id = Field(attribute='inner_id', column_name='inner_id', readonly=True, widget=widgets.CharWidget())
    reg_number = Field(attribute='reg_number', column_name='reg_number', readonly=True, widget=widgets.IntegerWidget())
    phone1 = Field(attribute='phone1', column_name='phone1', widget=widgets.CharWidget())
    phone2 = Field(attribute='phone2', column_name='phone2', widget=widgets.CharWidget())
    email = Field(attribute='email', column_name='email', widget=widgets.CharWidget())
    title = Field(attribute='title', column_name='title', widget=widgets.CharWidget())
    front_title = Field(attribute='front_title', column_name='front_title', widget=widgets.CharWidget())
    fullname = Field(attribute='fullname', column_name='fullname', widget=widgets.CharWidget())
    back_title = Field(attribute='back_title', column_name='back_title', widget=widgets.CharWidget())
    gender = Field(attribute='gender', column_name='gender', widget=widgets.CharWidget())
    religion = Field(attribute='religion', column_name='religion', widget=widgets.CharWidget())
    nation = Field(attribute='nation', column_name='nation', widget=widgets.CharWidget())
    place_of_birth = Field(attribute='place_of_birth', column_name='place_of_birth', widget=widgets.CharWidget())
    date_of_birth = Field(attribute='date_of_birth', column_name='date_of_birth',
                          widget=ExcelDateWidget(date_format='%d/%m/%Y'))
    last_education_level = Field(attribute='last_education_level', column_name='last_education_level', widget=widgets.CharWidget())
    last_education_institution = Field(attribute='last_education_institution', column_name='last_education_institution', widget=widgets.CharWidget())
    last_education_name = Field(attribute='last_education_name', column_name='last_education_name', widget=widgets.CharWidget())
    year_graduate = Field(attribute='year_graduate', column_name='year_graduate', widget=widgets.CharWidget())

    date_created = fields.Field(attribute='date_created', column_name='date_created',
                                widget=ExcelDateWidget(date_format='%d/%m/%Y %H:%M'))
    is_employee_applicant = fields.Field(attribute='is_employee_applicant',
                                         column_name='is_employee_applicant',
                                         widget=widgets.BooleanWidget())