from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from wagtail.core.models import Orderable
from modelcluster.models import ClusterableModel, ParentalKey

from wagtailkit.core.models import KitBaseModel, CreatorModelMixin
from wagtailkit.numerators.models import NumeratorMixin
from wagtailkit.persons.models import Person, Address, ContactInfo


class PersonAsPartnerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def get_partners(self):
        return super().get_queryset().filter(
            models.Q(partner__isnull=False))


class PersonAsPartner(Person):
    class Meta:
        proxy = True
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        permissions = (
            ('export_personaspartner', 'Can export Person as Partner'),
            ('import_personaspartner', 'Can import Person as Partner')
        )

    objects = PersonAsPartnerManager()

    @property
    def has_partner(self):
        partner = getattr(self, 'partner_set', None)
        return bool(partner)

    def __str__(self):
        return "{}".format(self.fullname)


class PartnerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def get_by_natural_key(self, inner_id):
        return self.get(inner_id=inner_id)


class Partner(ClusterableModel, NumeratorMixin, KitBaseModel, CreatorModelMixin):
    class Meta:
        verbose_name = _('Partner')
        verbose_name_plural = _('Partners')
        permissions = (
            ('export_partner', 'Can export Partner'),
            ('import_partner', 'Can import Partner')
        )

    doc_code = 'PRT'
    objects = PartnerManager()
    owner = models.OneToOneField(
        Person, null=True, blank=True,
        on_delete=models.CASCADE,
        verbose_name=_("Owner"))
    name = models.CharField(
        max_length=255, verbose_name=_('Partner name'),
        help_text=_('Partner name eg. Google .Inc or person name if partner is personal'))
    is_company = models.BooleanField(
        default=True, verbose_name=_("Company"))
    is_active = models.BooleanField(
        default=True, verbose_name=_("Active"))
    date_created = models.DateTimeField(
        null=True, blank=True,
        default=timezone.now,
        verbose_name=_('Created date'))

    @property
    def is_customer(self):
        customer = getattr(self, 'customer', None)
        return bool(customer)

    @property
    def is_supplier(self):
        supplier = getattr(self, 'supplier', None)
        return bool(supplier)

    @property
    def full_address(self):
        address = self.get_primary_address()
        line1 = []
        if address.street1:
            line1.append(address.street1)
        if address.street2:
            line1.append(address.street2)

        line2 = []
        if address.zipcode:
            line2.append(address.city)
        if address.province:
            line2.append(address.province)
        if address.country:
            line2.append(address.country)
        if address.zipcode:
            line2.append(address.zipcode)

        line1 = " ".join(line1)
        line2 = ", ".join(line2)
        return line1, line2

    @property
    def full_contactinfo(self):
        contact = self.get_contact_info()
        text = []
        text2 = []
        if contact.phone1:
            text.append('Phone: %s' % contact.phone1)
        if contact.fax:
            text.append('Fax: %s' % contact.fax)
        if contact.whatsapp:
            text.append('WA: %s' % contact.whatsapp)
        if contact.email:
            text2.append('Email: %s' % contact.email)
        if contact.website:
            text2.append('Website: %s' % contact.website)
        return ", ".join(text), ", ".join(text2)

    def __str__(self):
        return self.name

    def get_primary_address(self):
        address_set = getattr(self, 'partneraddress_set', None)
        primaries = address_set.filter(is_primary=True)
        return None if not primaries else primaries[0]

    def get_contact_info(self):
        contact_set = getattr(self, 'partnercontactinfo_set', None)
        contacts = contact_set.all()
        return None if not contacts else contacts[0]

    def natural_key(self):
        key = (self.inner_id,)
        return key


class PartnerContactInfo(Orderable, ContactInfo):
    class Meta:
        verbose_name = _('Contact Info')
        verbose_name_plural = _('Contact Info')

    partner = ParentalKey(
        Partner, on_delete=models.CASCADE,
        verbose_name=_('Partner'))


class PartnerAddress(Orderable, Address, KitBaseModel, CreatorModelMixin):
    class Meta:
        verbose_name = _('Billing Address')
        verbose_name_plural = _('Billing Address')

    partner = ParentalKey(
        Partner, on_delete=models.CASCADE,
        verbose_name=_('Partner'))
    is_primary = models.BooleanField(
        default=True, verbose_name=_('Primary'))
    name = models.CharField(
        null=True, blank=False,
        max_length=255,
        verbose_name=_("Name"), help_text=_('E.g. Shipping or Billing Address'))

    def __str__(self):
        return self.name

    @property
    def verbose_name(self):
        return "%s, %s" % (str(self.partner), self.name)


class ContactPersonBase(KitBaseModel):
    class Meta:
        abstract = True
        verbose_name = _('Contact Person')
        verbose_name_plural = _('Contact Persons')

    name = models.CharField(
        null=False, blank=False,
        max_length=255,
        verbose_name=_("Name"))
    phone = models.CharField(
        null=False, blank=False,
        max_length=255,
        verbose_name=_("Phone"))
    email = models.CharField(
        null=True, blank=True,
        max_length=255,
        verbose_name=_("Email"))
    department = models.CharField(
        null=True, blank=True,
        max_length=255,
        verbose_name=_("Department"))

    def __str__(self):
        return self.name


class CustomerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def get_by_natural_key(self, inner_id):
        return self.get(inner_id=inner_id)


class Customer(ClusterableModel, NumeratorMixin, CreatorModelMixin, KitBaseModel):
    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        permissions = (
            ('export_customer', 'Can export Customer'),
            ('import_customer', 'Can import Customer')
        )

    doc_code = 'CST'
    objects = CustomerManager()
    partner = models.OneToOneField(
        Partner,
        on_delete=models.CASCADE,
        verbose_name=_("Partner"))

    def __str__(self):
        return self.partner.name

    def natural_key(self):
        key = (self.inner_id,)
        return key


class CustomerContactPerson(Orderable, ContactPersonBase):
    class Meta:
        verbose_name = _('Contact Person')
        verbose_name_plural = _('Contact Persons')

    customer = ParentalKey(
        Customer, on_delete=models.CASCADE,
        related_name='customer_contactpersons',
        verbose_name=_('Customer')
    )


class SupplierManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def get_by_natural_key(self, inner_id):
        return self.get(inner_id=inner_id)


class Supplier(ClusterableModel, NumeratorMixin, CreatorModelMixin, KitBaseModel):
    class Meta:
        verbose_name = _('Supplier')
        verbose_name_plural = _('Suppliers')
        permissions = (
            ('export_supplier', 'Can export Supplier'),
            ('import_supplier', 'Can import Supplier')
        )

    doc_code = 'SUP'
    objects = SupplierManager()
    partner = models.OneToOneField(
        Partner,
        on_delete=models.CASCADE,
        verbose_name=_("Partner"))

    def __str__(self):
        return self.partner.name

    def natural_key(self):
        key = (self.inner_id,)
        return key


class SupplierContactPerson(Orderable, ContactPersonBase):
    class Meta:
        verbose_name = _('Sales Persons')
        verbose_name_plural = _('Sales Persons')

    supplier = ParentalKey(
        Supplier, on_delete=models.CASCADE,
        related_name='supplier_contactpersons',
        verbose_name=_('Supplier')
    )
