import uuid
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from wagtail.core.models import Orderable
from modelcluster.models import ClusterableModel, ParentalKey

from wagtailkit.core.models import KitBaseModel, CreatorModelMixin
from wagtailkit.numerators.models import NumeratorMixin
from wagtailkit.products.models import Product


class StockAdjustmentManager(models.Manager):

    def get_by_natural_key(self, inner_id):
        return self.get(inner_id=inner_id)

class StockAdjustment(ClusterableModel, NumeratorMixin, CreatorModelMixin, KitBaseModel):
    class Meta:
        verbose_name = _("Stock Adjustment")
        verbose_name_plural = _("Stock Adjustments")
        permissions = (
            ('validate_stockadjustment', _('Can validate Stock Adjustment')),
            ('reconcile_stockadjustment', _('Can reconcile Stock Adjustment')),
            ('print_stockadjustment', _('Can print Stock Adjustment')),
            ('edit_other_stockadjustment', _('Can edit other Stock Adjustment'))
        )

    doc_code = 'PRD.ADJ'

    title = models.CharField(
        max_length=255,
        verbose_name=_('Title'))
    description = models.CharField(
        max_length=255,
        verbose_name=_('Description'))
    effective_date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Effective date'))
    is_valid = models.BooleanField(
        default=False, verbose_name=_('Validated'))
    is_reconciled = models.BooleanField(
        default=False, verbose_name=_('Reconciled'))
    date_reconciled = models.DateTimeField(
        null=True, blank=True,
        verbose_name=_('Reconciled date'))
    reconciled_by = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT,
        null=True, blank=True,
        related_name='inventoryadjustment_reconciled_by',
        verbose_name=_("Reconciled by"))

    @property
    def is_editable(self):
        return not self.is_reconciled

    def natural_key(self):
        keys = (self.inner_id,)
        return keys

    def __str__(self):
        return self.title

    def validate(self):
        if self.adjusted_products.count() == 0:
            raise Exception(_('Please add 1 or more product!'))

        if not self.is_valid:
            self.is_valid = True
            self.save()
        else:
            raise Exception(_('Stock adjustment validated!'))

    def add_all_product(self, request):
        stockable_products = Product.objects.filter(is_stockable=True)
        if not self.is_reconciled:
            with transaction.atomic():
                create_products = []
                update_products = []
                item_added = self.adjusted_products.all()
                for product in stockable_products:
                    new_item = AdjustedProduct(
                        stock_adjustment=self,
                        product=product,
                        stock_on_hand=product.stockcard.stock_on_hand,
                        stock_scrapped=product.stockcard.stock_scrapped,
                    )
                    try:
                        added_product = item_added.get(stock_adjustment=self, product=product)
                        added_product.stock_on_hand = product.stock_on_hand
                        added_product.stock_scrapped = product.stock_scrapped
                        update_products.append(added_product)
                    except:
                        create_products.append(new_item)
                if create_products:
                    AdjustedProduct.objects.bulk_create(create_products)
                if update_products:
                    AdjustedProduct.objects.bulk_update(
                        update_products, ['stock_on_hand', 'stock_on_request', 'stock_on_delivery', 'stock_scrapped'])
                return create_products, update_products
        else:
            raise Exception(_('Stock adjustment reconciled!, adding more product is not allowed'))

    def reconcile(self, request):
        if self.is_valid and not self.is_reconciled:
            with transaction.atomic():
                # TODO optimize wit bulk_update !
                adjusted_products = self.adjusted_products.all()
                for adj_product in adjusted_products:
                    card = adj_product.product.stockcard
                    card.stock_on_hand = adj_product.new_stock_on_hand
                    card.stock_scrapped = adj_product.new_stock_scrapped
                    card.save()
                self.is_reconciled = True
                self.date_reconciled = timezone.now()
                self.reconciled_by = request.user
                self.save()
        else:
            if not self.is_valid:
                raise Exception(_('Please validate this stock adjustment!'))
            if self.is_reconciled:
                raise Exception(_('Stock adjustment reconciled!'))

class AdjustedProduct(Orderable, KitBaseModel):
    class Meta:
        verbose_name = _("Adjusted Product")
        verbose_name_plural = _("Adjusted Products")
        unique_together = ('stock_adjustment', 'product')
        index_together = ('stock_adjustment', 'product')

    stock_adjustment = ParentalKey(
        StockAdjustment,
        on_delete=models.CASCADE,
        related_name='adjusted_products',
        verbose_name=_("Stock Adjustment"))
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        verbose_name=_("Product"))

    stock_on_hand = models.PositiveIntegerField(
        default=0, verbose_name=_('Stock'))
    stock_scrapped = models.PositiveIntegerField(
        default=0, verbose_name=_('Scrapped'))

    new_stock_on_hand = models.PositiveIntegerField(
        default=0, verbose_name=_('New Stock'))
    new_stock_scrapped = models.PositiveIntegerField(
        default=0, verbose_name=_('New Scrapped'))

    def __str__(self):
        return str(self.product)
