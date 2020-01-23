from import_export.resources import ModelResource
from import_export import fields, widgets

from wagtailkit.importexport.widgets import UUIDWidget

from wagtailkit.persons.models import Person
from .models import Partner, Customer, Supplier


class PartnerResource(ModelResource):
    class Meta:
        model = Partner
        fields = ('id', 'inner_id', 'name', 'is_company', 'is_active')

    id = fields.Field(
        attribute='id',
        column_name='id',
        widget=UUIDWidget())
    owner = fields.Field(
        attribute='owner',
        column_name='owner',
        widget=widgets.ForeignKeyWidget(
            Person, field='inner_id'))
    owner_name = fields.Field(
        attribute='owner__fullname',
        column_name='owner_name',
        readonly=True,
        widget=widgets.CharWidget())
    inner_id = fields.Field(
        attribute='inner_id',
        column_name='inner_id',
        readonly=True,
        widget=widgets.CharWidget())


class CustomerResource(ModelResource):
    class Meta:
        model = Customer
        exclude = ('date_modified', 'date_created', 'creator', 'reg_number',)

    id = fields.Field(attribute='id', column_name='id', widget=UUIDWidget())
    inner_id = fields.Field(attribute='inner_id', column_name='inner_id', readonly=True, widget=widgets.CharWidget())
    partner = fields.Field(
        attribute='partner',
        column_name='partner',
        widget=widgets.ForeignKeyWidget(
            Partner, field='inner_id'))


class SupplierResource(ModelResource):
    class Meta:
        model = Supplier
        exclude = ('date_modified',)

    id = fields.Field(attribute='id', column_name='id', widget=UUIDWidget())
    inner_id = fields.Field(attribute='inner_id', column_name='inner_id', readonly=True, widget=widgets.CharWidget())
    partner = fields.Field(
        attribute='partner',
        column_name='partner',
        widget=widgets.ForeignKeyWidget(
            Partner, field='inner_id'))
