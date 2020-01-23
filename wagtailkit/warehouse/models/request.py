from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from wagtail.core.models import ClusterableModel, Orderable
from wagtail.core.fields import RichTextField
from modelcluster.fields import ParentalKey

from wagtailkit.core.models import (
    MAX_LEN_SHORT, MAX_LEN_MEDIUM, MAX_LEN_LONG, MAX_RICHTEXT,
    CreatorModelMixin, FiveStepStatusMixin, KitBaseModel)
from wagtailkit.numerators.models import NumeratorMixin
from wagtailkit.products.models import Product, Inventory, Asset


class RequestOrder(NumeratorMixin, ClusterableModel, FiveStepStatusMixin, CreatorModelMixin, KitBaseModel):
    class Meta:
        verbose_name = _("Request Order")
        verbose_name_plural = _("Request Orders")
        ordering = ['-date_created']
        index_together = ['date_created', 'creator']
        permissions = (
            ('trash_requestorder', _('Can trash Request Order')),
            ('draft_requestorder', _('Can draft Request Order')),
            ('validate_requestorder', _('Can validate Request Order')),
            ('approve_requestorder', _('Can approve Request Order')),
            ('reject_requestorder', _('Can reject Request Order')),
            ('process_requestorder', _('Can process Request Order')),
            ('complete_requestorder', _('Can complete Request Order')),
            ('close_requestorder', _('Can close Request Order')),
            ('print_requestorder', _('Can print Request Order')),
            ('changeother_requestorder', _('Can change other Request Order')),
            ('viewother_requestorder', _('Can view other Request Order')),
        )

    NORMAL = 'NRM'
    URGENT = 'URG'
    CRITICAL = 'CRT'
    CRIT_STATUS = (
        (NORMAL, _('Normal')),
        (URGENT, _('Urgent')),
        (CRITICAL, _('Critical')),
    )

    doc_code = 'FPB'

    requester = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Requester"))
    department = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Department"))
    deliver_to = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Deliver to"))
    title = models.CharField(
        max_length=MAX_LEN_LONG,
        verbose_name=_("Purpose of use"))
    description = RichTextField(
        default="""
        <p>Mohon dipenuhi permintaan persediaan dan asset berikut ini.<p/>
        <p><strong>Terima Kasih</strong></p>
        """,
        max_length=MAX_RICHTEXT,
        verbose_name=_("Description"))
    rejection_note = RichTextField(
        null=True, blank=True,
        max_length=MAX_RICHTEXT,
        verbose_name=_("Rejection note"))
    critical_status = models.CharField(
        max_length=3, choices=CRIT_STATUS, default=NORMAL,
        verbose_name=_("Status"))
    deadline = models.DateTimeField(
        default=timezone.now, verbose_name=_("On Deadline"))

    autocomplete_search_field = 'inner_id'

    def autocomplete_label(self):
        return "{} ({}/{})".format(self.inner_id, self.requester, self.status.title())

    def __str__(self):
        return self.inner_id

    def clean_validate_action(self):
        inventories = self.requested_inventories.count()
        assets = self.requested_assets.count()
        new_products = self.requested_new_products.count()
        if not inventories and not assets and not new_products:
            msg = _("Please add 1 or more product.")
            raise Exception(msg)

    def approve_validation(self):
        """ Check each product stock on hands for approval """
        for req_prd in self.requested_inventories.all():
            if req_prd.product.stockcard.stock < req_prd.quantity_approved:
                raise Exception("Sorry stock %s is %s " % (req_prd.product.name, req_prd.product.stock_on_hand))
        for req_prd in self.requested_assets.all():
            if req_prd.product.stockcard.stock < req_prd.quantity_approved:
                raise Exception("Sorry stock %s is %s " % (req_prd.product.name, req_prd.product.stock_on_hand))

    def update_on_request_stock(self):
        for req_prd in self.requested_inventories.all():
            req_prd.product.stockcard.stock_on_request += req_prd.quantity_approved
            req_prd.product.stockcard.save()
            req_prd.save()
        for req_prd in self.requested_assets.all():
            req_prd.product.stockcard.stock_on_request += req_prd.quantity_approved
            req_prd.product.stockcard.save()
            req_prd.save()

    def reset_on_request_stock(self):
        for req_prd in self.requested_inventories.all():
            req_prd.product.stockcard.stock_on_request -= req_prd.quantity_approved
            req_prd.product.stockcard.save()
            req_prd.save()
        for req_prd in self.requested_assets.all():
            req_prd.product.stockcard.stock_on_request -= req_prd.quantity_approved
            req_prd.product.stockcard.save()
            req_prd.save()

    def set_chairman_department(self):
        # Set chairman and department from user employee information
        # otherwise leave it blank
        if self.creator.is_person:
            employee = getattr(self.creator.person, 'employee', None)
            if employee:
                primary_chair = getattr(employee, 'primary_chair', None)
                if primary_chair:
                    self.requester = primary_chair.chair.position
                else:
                    self.requester = str(employee.person.fullname)
                self.department = employee.department.verbose_name
        else:
            self.requester = self.creator.fullname

    def clean(self):
        if self.status == 'approved':
            self.approve_validation()

    def save(self, *args, **kwargs):
        self.clean()
        self.set_chairman_department()
        super().save(*args, **kwargs)


class ProductRequestLineMixin(models.Model):
    class Meta:
        abstract = True

    quantity_requested = models.PositiveIntegerField(
        default=1, verbose_name=_("Quantity"),
        validators=[
            MinValueValidator(1, message=_('Minimum value is 1')),
            MaxValueValidator(1000, message=_('Maximum value is 1000'))
        ])
    quantity_approved = models.PositiveIntegerField(
        default=0, verbose_name=_("Approved quantity"),
        validators=[
            MinValueValidator(0, message=_('Minimum value is 0')),
            MaxValueValidator(1000, message=_('Maximum value is 1000'))
        ])


class InventoryRequestItem(CreatorModelMixin, Orderable, ProductRequestLineMixin, KitBaseModel):
    class Meta:
        verbose_name = _("Inventory Request Item")
        verbose_name_plural = _("Inventory Request Item")
        unique_together = ('request_order', 'product')

    request_order = ParentalKey(
        RequestOrder, on_delete=models.CASCADE,
        related_name='requested_inventories',
        verbose_name=_("Request order"))
    product = models.ForeignKey(
        Inventory, on_delete=models.PROTECT,
        verbose_name=_("Product"), )

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        self.clean()
        self.creator = self.request_order.creator
        super().save(*args, **kwargs)


class AssetRequestItem(Orderable, ProductRequestLineMixin, CreatorModelMixin, KitBaseModel):
    class Meta:
        verbose_name = _("Asset Request Item")
        verbose_name_plural = _("Asset Request Item")
        unique_together = ('request_order', 'product')

    request_order = ParentalKey(
        RequestOrder, on_delete=models.CASCADE,
        related_name='requested_assets',
        verbose_name=_("Request order"))
    product = models.ForeignKey(
        Asset, on_delete=models.PROTECT,
        verbose_name=_("Product"))

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        self.clean()
        self.creator = self.request_order.creator
        super().save(*args, **kwargs)
