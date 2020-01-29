from enum import Enum
from django.db import models
from django.utils import translation, timezone
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from wagtail.core.models import Orderable
from modelcluster.fields import ParentalKey

from wagtailkit.core.models import KitBaseModel, MAX_LEN_LONG
from wagtailkit.numerators.models import NumeratorMixin
from wagtailkit.products.models import Product, ProductCategory

_ = translation.gettext_lazy


class ServiceType(Enum):
    LAB = 'Laboratorium Uji'
    LIT = 'Inspeksi Teknis'
    KAL = 'Kalibrasi'
    LIB = 'Litbang'
    KSL = 'Konsultansi'
    PRO = 'Sertifikasi Produk'
    LAT = 'Pelatihan'
    LNY = 'Lainnya'


class TarifManager(models.Manager):
    def get_by_natural_key(self, inner_id):
        return self.get(inner_id=inner_id)


class Tarif(NumeratorMixin, KitBaseModel):
    class Meta:
        verbose_name = _('Tarif')
        verbose_name_plural = _('Tarifs')

    doc_code = 'TRF'
    objects = TarifManager()

    category = models.ForeignKey(
        ProductCategory, on_delete=models.PROTECT,
        verbose_name=_('Category'))
    service_type = models.CharField(
        max_length=3,
        choices=[(str(serv.name), serv.value) for serv in ServiceType],
        default=ServiceType.LAB,
        verbose_name=_('Service Type'))
    name = models.CharField(
        max_length=MAX_LEN_LONG,
        verbose_name=_('Name'))
    price = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name=_('Price'))
    date_effective = models.DateField(
        default=timezone.now,
        verbose_name=_('Date effective'))

    def __str__(self):
        return "{} - {}".format(self.category, self.name)

    def natural_key(self):
        keys = (self.inner_id,)
        return keys


class Fee(NumeratorMixin, KitBaseModel):
    class Meta:
        verbose_name = _('Fee')
        verbose_name_plural = _('Fees')

    doc_code = 'EXT'
    objects = TarifManager()

    name = models.CharField(
        max_length=MAX_LEN_LONG,
        verbose_name=_('Name'))
    price = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name=_('Price'))
    date_effective = models.DateField(
        default=timezone.now,
        verbose_name=_('Date effective'))

    def __str__(self):
        return self.name

    def natural_key(self):
        keys = (self.inner_id,)
        return keys


class LabService(Product):
    class Meta:
        verbose_name = _('Lab Service')
        verbose_name_plural = _('Lab Service')

    doc_code = 'LAB'

    service_type = models.CharField(
        max_length=3,
        choices=[(str(serv.name), serv.value) for serv in ServiceType],
        default=ServiceType.LAB,
        verbose_name=_('Service Type'))

    @property
    def parameters(self):
        params = getattr(self, 'product_parameters', None)
        return None if not params else params.all()

    @property
    def extra_fees(self):
        fees = getattr(self, 'product_fees', None)
        return None if not fees else fees.all()

    @property
    def total_fee(self):
        return self.calc_extra_fees()

    @property
    def total_tarif(self):
        return self.calc_tarif_prices()

    def natural_key(self):
        keys = (self.inner_id,)
        return keys

    natural_key.dependencies = ['silabis.user', 'sales.product', 'master.tarif']


    def get_doc_code(self):
        stype = getattr(ServiceType, str(self.service_type), 'PRD')
        return stype.name

    def calc_extra_fees(self):
        # Wagtail modelcluster FakeQuerySet doesn't support aggregate method
        return 0 if not self.extra_fees else sum(map(lambda x: x.price, self.extra_fees))

    def calc_tarif_prices(self):
        # Wagtail modelcluster FakeQuerySet doesn't support aggregate method
        return 0 if not self.parameters else sum(map(lambda x: x.price, self.parameters))

    def save(self, *args, **kwargs):
        self.unit_price = self.total_tarif + self.total_fee
        self.minimum_stock = 0
        self.maximum_stock = 0
        self.is_stockable = False
        self.is_consumable = False
        self.is_bundle = False
        self.is_sparepart = False
        super().save(*args, **kwargs)


class ExtraFee(Orderable, KitBaseModel):
    class Meta:
        verbose_name = _('Extra Fee')
        verbose_name_plural = _('Extra Fees')
        unique_together = ('product', 'fee')

    _ori_fee = None

    product = ParentalKey(
        LabService, related_name='product_fees',
        on_delete=models.CASCADE,
        verbose_name=_('Product'))
    fee = models.ForeignKey(
        Fee, on_delete=models.CASCADE,
        verbose_name=_('Extra Fee'))
    price = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name=_('Price'))
    date_effective = models.DateField(
        default=timezone.now,
        verbose_name=_('Date effective'))

    # TODO this is good, but wagtail raise recursion error
    @staticmethod
    @receiver(post_save, sender='simpellabproducts.ExtraFee')
    def after_save_update_product_price(sender, **kwargs):
        instance = kwargs.pop('instance', None)
        instance.product.save(commit_childs=False)

    @staticmethod
    @receiver(post_delete, sender='simpellabproducts.ExtraFee')
    def after_detele_update_product_price(sender, **kwargs):
        instance = kwargs.pop('instance', None)
        instance.product.save(commit_childs=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if getattr(self, 'fee', False):
            self._ori_fee = self.fee

    def __str__(self):
        return self.fee.name

    def clean(self):
        # TODO error with wagtail modelcluster
        # Make sure price don't change directly when fee price changed
        if self._state.adding is False and self._ori_fee != self.fee:
            msg = _("Fee can't be changed, please delete instead.")
            raise ValidationError({"fee": msg})
        pass

    def save(self, *args, **kwargs):
        self.clean()
        if not self.price:
            self.price = self.fee.price
        self.date_effective = self.fee.date_effective
        super().save(*args, **kwargs)


class Parameter(Orderable, KitBaseModel):
    class Meta:
        verbose_name = _('Parameter')
        verbose_name_plural = _('Parameters')
        unique_together = ('product', 'tarif')

    _ori_tarif = None

    product = ParentalKey(
        LabService, related_name='product_parameters',
        on_delete=models.CASCADE,
        verbose_name=_('Product'))
    tarif = models.ForeignKey(
        Tarif, on_delete=models.CASCADE,
        verbose_name=_('Parameter'))
    price = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name=_('Price'))
    date_effective = models.DateField(
        default=timezone.now,
        verbose_name=_('Date effective'))

    # TODO this is good, but wagtail raise recursion error
    @staticmethod
    @receiver(post_save, sender='simpellabproducts.Parameter')
    def after_save_update_product_price(sender, **kwargs):
        instance = kwargs.pop('instance', None)
        instance.product.save(commit_childs=False)

    @staticmethod
    @receiver(post_delete, sender='simpellabproducts.Parameter')
    def after_detele_update_product_price(sender, **kwargs):
        instance = kwargs.pop('instance', None)
        instance.product.save(commit_childs=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if getattr(self, 'tarif', False):
            self._ori_tarif = self.tarif

    def __str__(self):
        return self.tarif.name

    def clean(self):
        # Make sure product has matching tarifs
        product = getattr(self, 'product', None)
        tarif = getattr(self, 'tarif', None)
        service_tarif = {
            ServiceType.LAB.name: ['LAB', 'LIT'],
            ServiceType.LIT.name: ['LAB', 'LIT'],
            ServiceType.KAL.name: ['KAL'],
            ServiceType.PRO.name: ['PRO'],
            ServiceType.LAT.name: ['LAT'],
            ServiceType.LIB.name: ['LIB'],
            ServiceType.KSL.name: ['KSL'],
            ServiceType.LNY.name: ['LNY'],
        }
        if tarif and product:
            if self.tarif.service_type not in service_tarif[product.service_type]:
                msg = _("Please select {} tarif").format(", ".join(service_tarif[product.service_type]))
                raise ValidationError({"tarif": msg})

        # Todo Error in wagtail admin
        # Make sure price don't change directly when tarif price changed
        if self._state.adding is False and self._ori_tarif != self.tarif:
            msg = _("Tarif can't be changed, please delete instead.")
            raise ValidationError({"tarif": msg})
        pass

    def save(self, *args, **kwargs):
        self.clean()
        if not self.price:
            self.price = self.tarif.price
        self.date_effective = self.tarif.date_effective
        super().save(*args, **kwargs)
