from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from wagtailkit.sales.models import Order, OrderProduct


class LabOrder(Order):
    class Meta:
        proxy = True
        verbose_name = _('Lab Order')
        verbose_name_plural = _('Lab Orders')

    def save(self, *args, **kwargs):
        self.is_specific = True
        super().save(*args, **kwargs)


class LabOrderProduct(OrderProduct):
    class Meta:
        proxy = True
        verbose_name = _('Lab Order Item')
        verbose_name_plural = _('Lab Order Items')

    def clean(self):
        # Make sure product has matching tarifs
        order = getattr(self, 'order', None)
        product = getattr(self, 'product', None)
        # lab_order must be grouped
        product.is_specific = True
        if order and product:
            if getattr(order, 'is_specific', ):
                if product.service_type != order.order_type.code:
                    msg = _("Please select proper {} product")
                    raise ValidationError({"product": msg.format(order.order_type)})

        super().clean()

    @staticmethod
    @receiver(post_save, sender='simpellabsales.LabOrderProduct')
    def after_save_update_total_order(sender, **kwargs):
        instance = kwargs.pop('instance', None)
        instance.order.save(commit_childs=False)

    @staticmethod
    @receiver(post_delete, sender='simpellabsales.LabOrderProduct')
    def after_delete_update_total_order(sender, **kwargs):
        instance = kwargs.pop('instance', None)
        instance.order.save(commit_childs=False)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
