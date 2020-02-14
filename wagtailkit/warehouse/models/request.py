from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.auth.models import Group
from wagtail.core.models import ClusterableModel, Orderable
from wagtail.core.fields import RichTextField
from modelcluster.fields import ParentalKey

from mptt.models import TreeForeignKey

from wagtailkit.core.tasks import send_html_email
from wagtailkit.core.models import (
    MAX_LEN_MEDIUM, MAX_LEN_LONG, MAX_RICHTEXT,
    CreatorModelMixin, FiveStepStatusMixin, KitBaseModel)
from wagtailkit.numerators.models import NumeratorMixin
from wagtailkit.organizations.models import Position, Department
from wagtailkit.products.models import Inventory, Asset

warehouse_admins = Group.objects.get(name='Warehouse Admins')
warehouse_managers = Group.objects.get(name='Warehouse Managers')
warehouse_supervisors = Group.objects.get(name='Warehouse Supervisors')
warehouse_staffs = Group.objects.get(name='Warehouse Staffs')


class RequestOrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('requester', 'department', 'creator')

    def get_summary(self, requester=None, tree=False, date_start=None, date_end=None):
        filter = {}
        qs = self.get_queryset()
        if requester:
            if tree:
                filter.update({'requester__in': [requester] + list(requester.get_children())})
            else:
                filter.update({'requester': requester})
        if date_start and date_end:
            filter.update({'date_created__gte': date_start, 'date_created__lte': date_end})
        if filter:
            qs = qs.filter(**filter)
        return qs.aggregate(
            count_trash=models.Count('id', filter=models.Q(status=RequestOrder.TRASH)),
            count_draft=models.Count('id', filter=models.Q(status=RequestOrder.DRAFT)),
            count_valid=models.Count('id', filter=models.Q(status=RequestOrder.VALID)),
            count_approved=models.Count('id', filter=models.Q(status=RequestOrder.APPROVED)),
            count_rejected=models.Count('id', filter=models.Q(status=RequestOrder.REJECTED)),
            count_processed=models.Count('id', filter=models.Q(status=RequestOrder.PROCESS)),
            count_completed=models.Count('id', filter=models.Q(status=RequestOrder.COMPLETE)),
            count_close=models.Count('id', filter=models.Q(status=RequestOrder.CLOSED)),
            count_total=models.Count('id'),
        )


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
    objects = RequestOrderManager()

    requester = TreeForeignKey(
        Position, on_delete=models.PROTECT,
        related_name='position_wh_requests',
        verbose_name=_("Requester"))
    department = TreeForeignKey(
        Department, on_delete=models.PROTECT,
        related_name='department_wh_requests',
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

    def after_validate_action(self):
        """
            Send Email : Waiting For Approval
        """
        recipients = ['sasri.darmajaya@gmail.com']
        for user in warehouse_admins.user_set.all():
            recipients.append(user.email)
        for user in warehouse_managers.user_set.all():
            recipients.append(user.email)
        subject = _('Request Order #{} Approval')
        message_text = _("Request Order #{} waiting for approval, please visit this link to inspect and approve detail."
                         " <a href='{}{}'>Approve Request Order</a>")
        message = message_text.format(self.inner_id, settings.BASE_URL, self.get_absolute_admin_url())
        send_html_email(
            subject=subject.format(self.inner_id),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            message=message,
        )

    def after_reject_action(self):
        """
            Send Email Notification To Requester: Request Order Rejected
        """
        recipients = ['sasri.darmajaya@gmail.com']
        for user in warehouse_admins.user_set.all():
            recipients.append(user.email)
        recipients.append(self.creator.email)
        subject = _('Request Order #{} Rejected')
        message_text = _("Request Order #{} rejected, please visit this link to inspect detail."
                         " <a href='{}{}'>Inspect Request Order</a>")
        message = message_text.format(self.inner_id, settings.BASE_URL, self.get_absolute_admin_url())
        send_html_email(
            subject=subject.format(self.inner_id),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            message=message,
        )

    def after_approve_action(self):
        """
            Send Email Notification To Requester: Request Order Approved
        """
        recipients = ['sasri.darmajaya@gmail.com']
        for user in warehouse_admins.user_set.all():
            recipients.append(user.email)
        for user in warehouse_supervisors.user_set.all():
            recipients.append(user.email)
        for user in warehouse_staffs.user_set.all():
            recipients.append(user.email)
        recipients.append(self.creator.email)
        subject = _('Request Order #{} Approved')
        message_text = _("Request Order #{} approved, please visit this link to inspect approval detail."
                         " <a href='{}{}'> Approved Request Order</a>")
        message = message_text.format(self.inner_id, settings.BASE_URL, self.get_absolute_admin_url())
        send_html_email(
            subject=subject.format(self.inner_id),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            message=message,
        )

    def approve_validation(self):
        """ Check each product stock on hands for approval """
        for req_prd in self.requested_inventories.all():
            if req_prd.product.stockcard.stock < req_prd.quantity_approved:
                msg = "Sorry stock %s is %s " % (req_prd.product.name, req_prd.product.stockcard.stock)
                raise ValidationError(msg)
        for req_prd in self.requested_assets.all():
            if req_prd.product.stockcard.stock < req_prd.quantity_approved:
                msg = "Sorry stock %s is %s " % (req_prd.product.name, req_prd.product.stockcard.stock)
                raise ValidationError(msg)

    def after_process_action(self):
        """
            Send Email Notification To Requester: Request Order Processed
        """
        recipients = ['sasri.darmajaya@gmail.com']
        for user in warehouse_admins.user_set.all():
            recipients.append(user.email)
        recipients.append(self.creator.email)
        subject = _('Request Order #{} Processed')
        message_text = _("Request Order #{} processed, please visit this link to inspect detail."
                         " <a href='{}{}'>Inspect Request Order</a>")
        message = message_text.format(self.inner_id, settings.BASE_URL, self.get_absolute_admin_url())
        send_html_email(
            subject=subject.format(self.inner_id),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            message=message,
        )

    def after_complete_action(self):
        """
            Send Email Notification To Requester: Request Order Complete
        """
        recipients = ['sasri.darmajaya@gmail.com']
        for user in warehouse_admins.user_set.all():
            recipients.append(user.email)
        recipients.append(self.creator.email)
        subject = _('Request Order #{} Complete')
        message_text = _("Request Order #{} complete. Thanks.")
        message = message_text.format(self.inner_id, settings.BASE_URL, self.get_absolute_admin_url())
        send_html_email(
            subject=subject.format(self.inner_id),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            message=message,
        )

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

    def clean(self):
        if self.status == 'approved':
            self.approve_validation()

    def save(self, *args, **kwargs):
        self.clean()
        if self._state.adding:
            self.requester = self.creator.person.employee.position
            self.department = self.creator.person.employee.position.department
            self.deliver_to = self.creator.person.fullname
        super().save(*args, **kwargs)

    def get_absolute_admin_url(self):
        return reverse('warehouse_requestorder_modeladmin_inspect', args=(self.id,))


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
