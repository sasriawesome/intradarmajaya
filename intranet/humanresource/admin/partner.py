from django.contrib.admin.utils import quote, capfirst
from django.conf.urls import url
from django.shortcuts import get_object_or_404, reverse
from django.utils.translation import gettext_lazy as _

from wagtail.admin import messages
from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, TabbedInterface, ObjectList)

from wagtail.contrib.modeladmin.options import ModelAdmin

from wagtailkit.admin.views import CreateView
from wagtailkit.autocompletes.edit_handlers import AutocompletePanel
from wagtailkit.importexport.admin import ImportExportModelAdminMixin
from wagtailkit.partners.resources import PartnerResource, CustomerResource, SupplierResource
from wagtailkit.partners.models import PartnerPersonal, Partner, Customer, Supplier

from .person import PersonModelAdmin

class PartnerPersonalModelAdmin(PersonModelAdmin):
    menu_icon = 'fa-user'
    menu_label = _('Partner Personals')
    model = PartnerPersonal


class PartnerModelAdmin(ImportExportModelAdminMixin, ModelAdmin):
    model = Partner
    resource_class = PartnerResource
    create_view_class = CreateView
    menu_icon = 'fa-user'
    search_fields = ['name', 'inner_id']
    list_filter = ['date_created', 'is_active']
    list_display = ['inner_id', 'name', 'owner', 'is_customer', 'is_supplier', 'creator', 'date_created']

    def is_customer(self, instance):
        return instance.is_customer

    def is_supplier(self, instance):
        return instance.is_supplier

    is_customer.boolean = True
    is_supplier.boolean = True

    basic_panel = ObjectList([
        MultiFieldPanel([
            AutocompletePanel('owner'),
            FieldPanel('name'),
            FieldPanel('is_company'),
            FieldPanel('is_active'),
        ]),
    ], heading=_('Basic Informations'))

    contact_address = ObjectList([
        InlinePanel(
            'partnercontactinfo_set', max_num=1,
            panels=[
                MultiFieldPanel([
                    FieldPanel('phone1'),
                    FieldPanel('fax'),
                    FieldPanel('whatsapp'),
                    FieldPanel('email'),
                    FieldPanel('website')
                ])
            ]
        ),
    ], heading=_('Contacts'))

    address_panel = ObjectList([
        InlinePanel(
            'partneraddress_set',
            panels=[
                MultiFieldPanel([
                    FieldPanel('is_primary'),
                    FieldPanel('name'),
                    FieldPanel('street1'),
                    FieldPanel('street2'),
                    FieldPanel('city'),
                    FieldPanel('province'),
                    FieldPanel('country'),
                    FieldPanel('zipcode'),
                ])
            ]
        ),
    ], heading=_('Addresses'))

    edit_handler = TabbedInterface([
        basic_panel, contact_address, address_panel
    ])


class CustomerModelAdmin(ImportExportModelAdminMixin, ModelAdmin):
    model = Customer
    resource_class = CustomerResource
    create_view_class = CreateView
    menu_icon = 'fa-user'
    search_fields = ['name', 'inner_id']
    list_filter = ['date_created', 'partner__name']
    list_display = ['inner_id', 'partner', 'creator', 'date_created']

    edit_handler = ObjectList([
        MultiFieldPanel([
            AutocompletePanel('partner'),
        ], heading=_('Partner')),
        InlinePanel(
            'customer_contactpersons', heading=_('Contact persons'),
            panels=[
                MultiFieldPanel([
                    FieldPanel('name'),
                    FieldPanel('phone'),
                    FieldPanel('email'),
                    FieldPanel('department'),
                ])
            ]
        ),
    ])


class SupplierModelAdmin(ImportExportModelAdminMixin, ModelAdmin):
    model = Supplier
    resource_class = SupplierResource
    create_view_class = CreateView
    menu_icon = 'fa-user'
    search_fields = ['name', 'inner_id', 'partner__name']
    list_filter = ['date_created']
    list_display = ['inner_id', 'partner', 'creator', 'date_created']

    edit_handler = ObjectList([
        MultiFieldPanel([
            AutocompletePanel('partner'),
        ], heading=_('Partner')),
        InlinePanel(
            'supplier_contactpersons', heading=_('Contact persons'),
            panels=[
                MultiFieldPanel([
                    FieldPanel('name'),
                    FieldPanel('phone'),
                    FieldPanel('email'),
                    FieldPanel('department'),
                ])
            ]
        ),
    ])
