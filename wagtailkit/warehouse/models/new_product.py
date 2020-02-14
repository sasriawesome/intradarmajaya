from django.db import models
from django.utils import text, translation

from wagtail.core.fields import RichTextField
from wagtail.images.models import Image
from modelcluster.fields import ParentalKey

from mptt.models import TreeForeignKey

from wagtailkit.core.models import CreatorModelMixin, KitBaseModel
from wagtailkit.numerators.models import NumeratorMixin
from wagtailkit.products.models import ProductCategory
from .request import RequestOrder

_ = translation.gettext_lazy


class NewProduct(NumeratorMixin, CreatorModelMixin, KitBaseModel):
    class Meta:
        verbose_name = _('New Product')
        verbose_name_plural = _('New Products')

    doc_code = 'PRD.NEW'

    request = ParentalKey(
        RequestOrder, on_delete=models.CASCADE,
        related_name='requested_new_products',
        verbose_name=_('Request Order'))
    picture = models.ForeignKey(
        Image, null=True, blank=True,
        on_delete=models.SET_NULL)
    category = TreeForeignKey(
        ProductCategory, null=True, blank=True,
        on_delete=models.PROTECT, verbose_name=_("Category"))
    slug = models.SlugField(
        max_length=255,
        verbose_name=_('Slug'))
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'))
    quantity_requested = models.PositiveIntegerField(
        default=1, verbose_name=_('Quantity'))
    quantity_approved = models.PositiveIntegerField(
        default=0, verbose_name=_('Approved Quantity'))
    description = RichTextField(
        null=True, blank=True,
        max_length=1000,
        verbose_name=_('Description'))


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = text.slugify(self.name)
        super(NewProduct, self).save(*args, **kwargs)
