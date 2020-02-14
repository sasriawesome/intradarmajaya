import uuid
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

from polymorphic.models import PolymorphicModel, PolymorphicManager
from polymorphic.utils import get_base_polymorphic_model
from wagtail.core.models import Orderable, ClusterableModel
from modelcluster.fields import ParentalKey

from wagtailkit.core.models import (
    MAX_LEN_MEDIUM, MAX_LEN_SHORT,
    KitBaseModel, FourStepStatusMixin, CreatorModelMixin)
from wagtailkit.products.models import Inventory, Asset
from wagtailkit.numerators.models import Numerator, NumeratorMixin
from wagtailkit.warehouse.models import WarehouseLocation, RequestOrder

class ProductTransferManager(PolymorphicManager):

    def get_queryset(self):
        return super().get_queryset()

    def get_summary(self, date_start=None, date_end=None):
        qs = self.get_queryset()
        if date_start and date_end:
            qs = self.get_queryset().filter(date_created__gte=date_start, date_created__lte=date_end)
        return qs.aggregate(
            count_trash=models.Count('id', filter=models.Q(status=ProductTransfer.TRASH)),
            count_draft=models.Count('id', filter=models.Q(status=ProductTransfer.DRAFT)),
            count_valid=models.Count('id', filter=models.Q(status=ProductTransfer.VALID)),
            count_processed=models.Count('id', filter=models.Q(status=ProductTransfer.PROCESS)),
            count_completed=models.Count('id', filter=models.Q(status=ProductTransfer.COMPLETE)),
            count_close=models.Count('id', filter=models.Q(status=ProductTransfer.CLOSED)),
            count_total=models.Count('id'),
        )

class ProductTransfer(ClusterableModel, NumeratorMixin, FourStepStatusMixin,
                      CreatorModelMixin, PolymorphicModel, KitBaseModel):
    class Meta:
        verbose_name = _("Transfer")
        verbose_name_plural = _("Transfers")
        permissions = (
            ('trash_producttransfer', _('Can trash Product Transfer')),
            ('draft_producttransfer', _('Can draft Product Transfer')),
            ('validate_producttransfer', _('Can validate Product Transfer')),
            ('process_producttransfer', _('Can process Product Transfer')),
            ('complete_producttransfer', _('Can complete Product Transfer')),
            ('print_producttransfer', _('Can complete Product Transfer')),
        )

    IN = 'IN'
    OUT = 'OUT'
    REF = (
        (IN, 'Check in'),
        (OUT, 'Check out'),
    )

    objects = ProductTransferManager()

    reftype = models.CharField(
        max_length=3, choices=REF, default=IN,
        verbose_name=_('Transfer'))
    title = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_('Title'))
    description = models.CharField(
        null=True, blank=True,
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_('Description'))

    def __str__(self):
        return str(self.inner_id)

    @property
    def is_editable(self):
        return self.status in ['draft', 'trash']

    def get_reference(self):
        return self.get_real_instance().reference

    def get_real_class_verbose_name(self):
        return self.get_real_instance()._meta.verbose_name

    def clean_validate_action(self):
        # Make sure all transfer item is valid
        inventories = getattr(self, 'inventory_transfers')
        assets = getattr(self, 'asset_transfers')
        if inventories:
            inventories = inventories.count()
        if assets:
            assets = assets.count()
        if inventories == 0 and assets == 0:
            msg = _("Please add 1 or more product.")
            raise ValueError(msg)

    def validate_and_process_reference(self, request):
        raise NotImplementedError

    def get_counter(self):
        # Get ContentTypeCounter instance for this model
        base_model = get_base_polymorphic_model(self._meta.model)
        parent = None if self.__class__ == 'Product' else base_model
        ct_counter = Numerator.get_instance(self, model=parent)
        return ct_counter


class TransferCheckIn(ProductTransfer):
    class Meta:
        verbose_name = _("Check In")
        verbose_name_plural = _("Check Ins")
        permissions = (
            ('trash_transfercheckin', _('Can trash Transfer Check In')),
            ('draft_transfercheckin', _('Can draft Transfer Check In')),
            ('validate_transfercheckin', _('Can validate Transfer Check In')),
            ('process_transfercheckin', _('Can process Transfer Check In')),
            ('complete_transfercheckin', _('Can complete Transfer Check In')),
            ('print_transfercheckin', _('Can complete Transfer Check In')),
        )

    doc_code = 'FTB'

    reference = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Reference"))
    sender = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Sender"))
    department = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Department"))
    received_date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("Date received"))

    def validate_and_process_reference(self, request):
        with transaction.atomic():
            self.validate()

    def complete_and_sync_stock(self, request):
        with transaction.atomic():
            for item in self.inventory_transfers.all():
                item.product.stockcard.stock_on_hand += item.quantity
                item.product.stockcard.save()
            for item in self.asset_transfers.all():
                item.product.stockcard.stock_on_hand += item.quantity
                item.product.stockcard.save()
            self.complete()

    def save(self, *args, **kwargs):
        self.reftype = ProductTransfer.IN
        super().save(**kwargs)


class TransferCheckOut(ProductTransfer):
    class Meta:
        verbose_name = _("Check Out")
        verbose_name_plural = _("Check Outs")
        ordering = ['-date_created']
        permissions = (
            ('trash_transfercheckout', _('Can trash Transfer Check Out')),
            ('draft_transfercheckout', _('Can draft Transfer Check Out')),
            ('validate_transfercheckout', _('Can validate Transfer Check Out')),
            ('process_transfercheckout', _('Can process Transfer Check Out')),
            ('complete_transfercheckout', _('Can complete Transfer Check Out')),
            ('print_transfercheckout', _('Can complete Transfer Check Out')),
        )

    doc_code = 'FBK'

    request_order = models.OneToOneField(
        RequestOrder,
        on_delete=models.PROTECT,
        verbose_name=_('Request Order'))
    requester = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Requester"))
    department = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Department"))
    deliver_to = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Deliver to"))
    delivered_date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("Date delivered"))

    def validate_and_process_reference(self, request):
        with transaction.atomic():
            self.validate()
            self.request_order.process()

    def complete_and_sync_stock(self, request):
        with transaction.atomic():
            for item in self.inventory_transfers.all():
                item.product.stockcard.stock_on_hand -= item.quantity
                item.product.stockcard.save()
            for item in self.asset_transfers.all():
                item.product.stockcard.stock_on_hand -= item.quantity
                item.product.stockcard.save()
            self.request_order.reset_on_request_stock()
            self.request_order.complete()
            self.complete()

    def clean(self):
        super().clean()
        if self._state.adding and self.request_order.status != RequestOrder.APPROVED:
            raise ValidationError({"request_order": _("Request order status is not approved")})

    def save(self, *args, **kwargs):
        self.reftype = ProductTransfer.OUT
        self.requester = self.request_order.requester.name
        self.department = self.request_order.department.name
        self.deliver_to = self.request_order.deliver_to
        self.clean()
        return super().save(**kwargs)


class TransferScrapped(ProductTransfer):
    class Meta:
        verbose_name = _("Scrapped")
        verbose_name_plural = _("Scrappeds")
        permissions = (
            ('trash_transferscrapped', _('Can trash Transfer Scrapped')),
            ('draft_transferscrapped', _('Can draft Transfer Scrapped')),
            ('validate_transferscrapped', _('Can validate Transfer Scrapped')),
            ('process_transferscrapped', _('Can process Transfer Scrapped')),
            ('complete_transferscrapped', _('Can complete Transfer Scrapped')),
            ('print_transferscrapped', _('Can complete Transfer Scrapped')),
        )

    doc_code = 'FBR'

    remover = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Remover"))
    reference = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Reference"))
    location = models.ForeignKey(
        WarehouseLocation, null=True, blank=False,
        on_delete=models.PROTECT,
        verbose_name=_('Location'))
    scrapped_date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("Date scrapped"))

    def validate_and_process_reference(self, request):
        with transaction.atomic():
            for item in self.inventory_transfers.all():
                item.clean_for_validation()
            for item in self.asset_transfers.all():
                item.clean_for_validation()
            self.validate()

    def complete_and_sync_stock(self, request):
        with transaction.atomic():
            for item in self.inventory_transfers.all():
                item.product.stockcard.stock_on_hand -= item.quantity
                item.product.stockcard.stock_scrapped += item.quantity
                item.product.stockcard.save()
            for item in self.asset_transfers.all():
                item.product.stockcard.stock_on_hand -= item.quantity
                item.product.stockcard.stock_scrapped += item.quantity
                item.product.stockcard.save()
            self.complete()

    def save(self, *args, **kwargs):
        self.reftype = ProductTransfer.OUT
        self.clean()
        return super().save(**kwargs)


class TransferLineValidation:
    def clean(self):
        # Validation for checkout and scrapped item
        producttransfer = getattr(self, 'producttransfer', None)
        if producttransfer:
            # Validate stock readiness
            if producttransfer.reftype == 'OUT' and self.product.stockcard.stock_on_hand < self.quantity:
                msg_text = _('Not enough stock, Current %s stock on hand is %s checkout quantity is %s')
                msg = msg_text % (
                    str(self.product),
                    str(self.product.stockcard.stock_on_hand),
                    str(self.quantity),
                )
                raise ValidationError(msg)


class InventoryTransferLine(TransferLineValidation, Orderable, KitBaseModel):
    class Meta:
        verbose_name = _("Inventory Check In")
        verbose_name_plural = _("Inventory Check Ins")
        unique_together = ('producttransfer', 'product')

    producttransfer = ParentalKey(
        ProductTransfer, on_delete=models.CASCADE,
        related_name='inventory_transfers',
        verbose_name=_("Product transfer"))
    product = models.ForeignKey(
        Inventory, on_delete=models.PROTECT,
        verbose_name=_("Product"))
    quantity = models.PositiveIntegerField(
        default=1, verbose_name=_("Quantity"),
        validators=[
            MinValueValidator(1, message=_('Minimum value is 1')),
            MaxValueValidator(1000, message=_('Maximum value is 1000'))
        ])

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)


class AssetTransferLine(TransferLineValidation, Orderable, KitBaseModel):
    class Meta:
        verbose_name = _("Asset Transfer")
        verbose_name_plural = _("Asset Transfers")
        unique_together = ('producttransfer', 'product')

    producttransfer = ParentalKey(
        ProductTransfer, on_delete=models.CASCADE,
        related_name='asset_transfers',
        verbose_name=_("Product transfer"))
    product = models.ForeignKey(
        Asset, on_delete=models.PROTECT,
        verbose_name=_("Product"))
    quantity = models.PositiveIntegerField(
        default=1, verbose_name=_("Quantity"),
        validators=[
            MinValueValidator(1, message=_('Minimum value is 1')),
            MaxValueValidator(1000, message=_('Maximum value is 1000'))
        ])

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)
