from django.db import models
from django.utils import translation
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from wagtail.core.models import Orderable
from modelcluster.models import ParentalKey

from wagtailkit.core.utils.text import number_to_text_id
from wagtailkit.core.models import (
    KitBaseModel, CreatorModelMixin,
    FourStepStatusMixin, SignalAwareClusterableModel,
    MAX_LEN_MEDIUM, MAX_LEN_LONG)
from wagtailkit.numerators.models import NumeratorMixin
from wagtailkit.partners.models import Customer
from wagtailkit.products.models import Product

_ = translation.gettext_lazy


class OrderManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs


class OrderType(models.Model):
    class Meta:
        verbose_name = _('Order Type')
        verbose_name_plural = _('Order Types')

    code = models.CharField(unique=True, primary_key=True, max_length=5)
    name = models.CharField(max_length=MAX_LEN_MEDIUM, verbose_name=_('name'))

    def __str__(self):
        return self.name


class Order(SignalAwareClusterableModel, NumeratorMixin, FourStepStatusMixin, CreatorModelMixin, KitBaseModel):
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        permissions = (
            ('draft_order', _('Can draft Order')),
            ('trash_order', 'Can trash Order'),
            ('validate_order', 'Can validate Order'),
            ('process_order', 'Can process Order'),
            ('complete_order', 'Can complete Order'),
            ('invoice_order', 'Can invoice Order'),
            ('close_order', 'Can close Order'),
        )

    objects = OrderManager()

    doc_code = 'SPJ'

    is_specific = models.BooleanField(
        default=False, editable=False,
        verbose_name=_('Is specific'),
        help_text=_('Group product order by order type'))
    order_type = models.ForeignKey(
        OrderType, null=True, blank=False,
        on_delete=models.PROTECT,
        verbose_name=_('Type'))
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT,
        verbose_name=_('Customer'))
    customer_po = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        null=True, blank=True,
        verbose_name=_('Customer PO'))
    note = models.CharField(
        max_length=MAX_LEN_LONG,
        null=True, blank=True,
        verbose_name=_("Note"))
    total_order = models.DecimalField(
        default=0, max_digits=15,
        decimal_places=2,
        verbose_name=_('Total Order'))
    discount_percentage = models.DecimalField(
        default=0, max_digits=15,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ], verbose_name=_('Discount'),
        help_text=_('Discount in percent'))
    discount = models.DecimalField(
        default=0, max_digits=15,
        decimal_places=2,
        verbose_name=_('Total discount'))
    grand_total = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name=_('Grand Total'))

    def __str__(self):
        return "{} ({})".format(self.inner_id, self.customer.partner.name)

    @property
    def products(self):
        products = getattr(self, 'order_products', None)
        return None if not products else products.all()

    @property
    def grand_total_text(self):
        return number_to_text_id(self.grand_total)

    def calc_total_order(self):
        self.total_order = 0 if not self.products else sum(map(lambda x: x.total_price, self.products))
        return self.total_order

    def calc_total_discount(self):
        self.discount = ((self.total_order * self.discount_percentage) / 100)

    def calc_grand_total(self):
        self.grand_total = self.total_order - self.discount

    def calc_all_total(self):
        self.calc_total_order()
        self.calc_total_discount()
        self.calc_grand_total()

    def save(self, *args, **kwargs):
        self.calc_all_total()
        super().save(*args, **kwargs)


class OrderProduct(Orderable, KitBaseModel):
    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')
        ordering = ('product',)
        unique_together = ('order', 'product')

    _ori_product = None

    order = ParentalKey(
        Order, related_name='order_products',
        on_delete=models.CASCADE,
        verbose_name=_('Order'))
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='order_items')
    unit_price = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name=_('Product price'))
    quantity = models.PositiveIntegerField(
        default=1, verbose_name=_('Quantity'),
        validators=[
            MinValueValidator(1, message=_('Minimal value: 1')),
            MaxValueValidator(500, message=_('Maximal value: 500'))
        ])
    total_price = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name=_('Total Price'))

    @staticmethod
    @receiver(post_save, sender='sales.OrderProduct')
    def after_save_update_total_order(sender, **kwargs):
        instance = kwargs.pop('instance', None)
        instance.order.save(commit_childs=False)

    @staticmethod
    @receiver(post_delete, sender='sales.OrderProduct')
    def after_delete_update_total_order(sender, **kwargs):
        instance = kwargs.pop('instance', None)
        instance.order.save(commit_childs=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if getattr(self, 'product', False):
            self._ori_product = self.product

    def __str__(self):
        return self.product.name

    def clean(self):
        # Make sure price don't change directly when tarif price changed
        if self._state.adding is False and self._ori_product.id != self.product.id:
            msg = _("Product can't be changed, please delete instead.")
            raise ValidationError({"product": msg})

    def save(self, *args, **kwargs):
        product = self.product.get_real_instance()
        self.unit_price = product.unit_price
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)
