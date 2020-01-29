from django.contrib import admin
from django.utils import translation

from wagtailkit.partners.models import (
    PersonAsPartner, Partner, Customer, Supplier,
    PartnerContactInfo,
    PartnerAddress)

_ = translation.gettext_lazy


class PartnerInline(admin.TabularInline):
    model = Partner
    can_delete = False


@admin.register(PersonAsPartner)
class OwnerAdmin(admin.ModelAdmin):
    show_in_index = True
    search_fields = ['person__name', 'partner__name']
    list_display = ['fullname']
    inlines = [PartnerInline]


class PartnerContactInfoInline(admin.StackedInline):
    max_num = 1
    extra = 1
    model = PartnerContactInfo


class PartnerAddressInline(admin.StackedInline):
    extra = 1
    max_num = 2
    model = PartnerAddress


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    show_in_index = True
    search_fields = ['owner__company__name']
    list_display = [
        'inner_id', 'name', 'owner',
        'is_customer', 'is_supplier',
        'is_active', 'date_created']
    inlines = [PartnerContactInfoInline, PartnerAddressInline]


admin.site.register(Customer)
admin.site.register(Supplier)