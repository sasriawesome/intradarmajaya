from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.dispatch import receiver

from mptt.models import MPTTModel, TreeForeignKey

from wagtail.search import index

from wagtailkit.core.models.settings import CompanySettings
from wagtailkit.core.models import KitBaseModel, MAX_LEN_MEDIUM, MAX_LEN_SHORT
from wagtailkit.numerators.models import NumeratorMixin
from wagtailkit.products.models import Product, Inventory, Asset


class WarehouseLocation(index.Indexed, MPTTModel):
    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")

    PHYSICAL = 'PSC'
    VIRTUAL = 'VRT'
    LOC_TYPE = (
        (PHYSICAL, _('Physical')),
        (VIRTUAL, _('Virtual')),
    )

    parent = TreeForeignKey(
        'WarehouseLocation',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Parent'))
    code = models.CharField(
        max_length=MAX_LEN_SHORT,
        verbose_name=_('Code'))
    name = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_('Name'))
    loc_type = models.CharField(
        max_length=MAX_LEN_SHORT,
        choices=LOC_TYPE, default=PHYSICAL,
        verbose_name=_('Location type'))

    search_fields = [
        index.SearchField('name', partial_match=True)
    ]

    def __str__(self):
        return self.name


class ProductStorage(KitBaseModel, NumeratorMixin):
    class Meta:
        verbose_name = _("Product Storage")
        verbose_name_plural = _("Product Storages")

    doc_code = 'PR.STG'

    parent = TreeForeignKey(
        WarehouseLocation,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Location'))
    name = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_('Storage name'))
    products = models.ManyToManyField(
        Product, related_name='storage_location',
        verbose_name=_('Products')
    )

    def __str__(self):
        return self.name


class StockCard(KitBaseModel):
    class Meta:
        verbose_name = _('Stock Card')
        verbose_name_plural = _('Stock Cards')

    product = models.OneToOneField(
        Product, on_delete=models.CASCADE,
        verbose_name=_('Product'))
    stock_on_hand = models.PositiveIntegerField(
        default=0, verbose_name=_("On hand"))
    stock_on_request = models.PositiveIntegerField(
        default=0, verbose_name=_("On request"))
    stock_on_delivery = models.PositiveIntegerField(
        default=0, verbose_name=_("On delivery"))
    stock_scrapped = models.PositiveIntegerField(
        default=0, verbose_name=_("Scrapped"))

    @staticmethod
    @receiver(post_save, sender=Inventory)
    def create_inventory_stock_card(sender, **kwargs):
        """ Create stock card when new Inventory created """
        created = kwargs.pop('created', False)
        instance = kwargs.pop('instance', None)
        if created:
            StockCard.objects.create(
                product=instance,
            )

    @staticmethod
    @receiver(post_save, sender=Asset)
    def create_asset_stock_card(sender, **kwargs):
        """ Create stock card when new Asset created """
        created = kwargs.pop('created', False)
        instance = kwargs.pop('instance', None)
        if created:
            StockCard.objects.create(
                product=instance,
            )

    @property
    def stock_min(self):
        return self.product.minimum_stock

    @property
    def stock_max(self):
        return self.product.maximum_stock

    @property
    def unit_price(self):
        return self.product.unit_price

    @property
    def total_price(self):
        return self.stock_on_hand * self.unit_price

    @property
    def stock(self):
        qty = (
            self.stock_on_hand
            - self.stock_on_request
            + self.stock_on_delivery
        )
        return qty

    def get_history_queryset(self, request, date_from=None, date_until=None):
        """
            Get Stock history beetween two dates
        """
        real_instance = self.product.get_real_instance()
        adjustment = real_instance.adjustedproduct_set.all()
        settings = CompanySettings.for_site(request.site)
        fcl_start = settings.fiscal_year_start
        fcl_end = settings.fiscal_year_end
        fcl_start_datetime = timezone.datetime(
            fcl_start.year, fcl_start.month, fcl_start.day, hour=0, minute=0, second=0)
        fcl_end_datetime = timezone.datetime(
            fcl_end.year, fcl_end.month, fcl_end.day, hour=23, minute=59, second=59)
        date_from = date_from or fcl_start_datetime or timezone.datetime(2010, 1, 1, hour=0, minute=0, second=0)
        date_until = date_until or fcl_end_datetime or timezone.now()

        if isinstance(real_instance, Inventory):
            transfer_line = real_instance.inventorytransferline_set.all()
        else:
            transfer_line = real_instance.assettransferline_set.all()

        transfers = transfer_line.filter(
            date_created__gte=date_from,
            date_created__lte=date_until,
            producttransfer__status='complete'
        ).values('id').annotate(
            date=models.F('producttransfer__date_created'),
            flow=models.F('producttransfer__reftype'),
            reference=models.F('producttransfer__inner_id'),
            memo=models.F('producttransfer__title'),
            qty=models.F('quantity'),
        )

        adjustments = adjustment.filter(
            date_created__gte=date_from,
            date_created__lte=date_until,
            stock_adjustment__is_reconciled=True
        ).values('id').annotate(
            date=models.F('stock_adjustment__effective_date'),
            flow=models.Value('IN', output_field=models.CharField()),
            reference=models.F('stock_adjustment__inner_id'),
            memo=models.F('stock_adjustment__title'),
            qty=models.F('new_stock_on_hand'),
        )

        return adjustments.union(transfers).order_by('date')

    def get_history_items(self, request, date_from=None, date_until=None):
        histories = self.get_history_queryset(request, date_from, date_until)
        results = []
        stock = 0
        for res in histories:
            if res['flow'] == 'IN':
                stock += res['qty']
                res['stock'] = stock
            else:
                stock -= res['qty']
                res['stock'] = stock
            results.append(res)
        return results

    def __str__(self):
        return self.product.name
