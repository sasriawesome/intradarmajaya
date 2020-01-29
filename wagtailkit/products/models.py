from django.db import models
from django.utils import text, translation

from wagtail.core.models import Orderable, ClusterableModel
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel, ObjectList
from wagtail.snippets.models import register_snippet
from wagtail.images.models import Image
from wagtail.search import index
from modelcluster.fields import ParentalKey

from mptt.models import TreeForeignKey, TreeManager, MPTTModel
from taggit.models import TaggedItemBase
from polymorphic.models import PolymorphicModel, PolymorphicManager
from polymorphic.utils import get_base_polymorphic_model

from wagtailkit.core.models import CreatorModelMixin, KitBaseModel, SignalAwareClusterableModel
from wagtailkit.numerators.models import NumeratorMixin, Numerator
from wagtailkit.partners.models import Partner, Supplier, Customer

_ = translation.gettext_lazy


class SnippetBaseManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class SnippetBase(index.Indexed, KitBaseModel):
    """ Base snippet """

    class Meta:
        abstract = True

    objects = SnippetBaseManager()

    name = models.CharField(
        max_length=255,
        unique=True, verbose_name=_('Name'))
    description = models.TextField(
        null=True, blank=True,
        max_length=512,
        verbose_name=_('Description'))

    search_fields = [
        index.SearchField('name', partial_match=True),
    ]

    edit_handler = ObjectList([
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('description'),
        ])
    ])

    def __str__(self):
        return self.name

    def natural_key(self):
        key = (self.name,)
        return key


@register_snippet
class PaymentMethod(SnippetBase):
    class Meta:
        verbose_name = _('Payment Method')
        verbose_name_plural = _('Payment Methods')


@register_snippet
class DeliveryMethod(SnippetBase):
    class Meta:
        verbose_name = _('Delivery Method')
        verbose_name_plural = _('Delivery Methods')


@register_snippet
class UnitOfMeasure(SnippetBase):
    class Meta:
        verbose_name = _('Unit of measure')
        verbose_name_plural = _('Unit of measures')


class ProductCategoryManager(TreeManager):
    def get_queryset(self):
        return super().get_queryset()

    def get_by_natural_key(self, name):
        return self.get(name=name)


@register_snippet
class ProductCategory(index.Indexed, MPTTModel, KitBaseModel):
    class Meta:
        verbose_name = _('Product Category')
        verbose_name_plural = _('Product Categories')

    objects = ProductCategoryManager()

    slug = models.SlugField(
        null=True, blank=True,
        max_length=255,
        unique=True, verbose_name=_('Slug'))
    name = models.CharField(
        max_length=255,
        unique=True, verbose_name=_('Name'))
    parent = TreeForeignKey(
        'products.ProductCategory',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Parent'))

    search_fields = [
        index.SearchField('name', partial_match=True),
    ]

    edit_handler = ObjectList([
        MultiFieldPanel([
            FieldPanel('parent'),
            FieldPanel('slug'),
            FieldPanel('name'),
        ])
    ])

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.slug in [None, ''] and self.name:
            self.slug = self.name
        self.slug = text.slugify(self.slug.lower())
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields)

    def natural_key(self):
        keys = (self.name,)
        return keys


class ProductTag(TaggedItemBase):
    content_object = ParentalKey(
        'products.Product',
        related_name='tagged_products',
        on_delete=models.CASCADE
    )


class ProductManager(PolymorphicManager):
    def get_by_natural_key(self, inner_id):
        return self.get(inner_id=inner_id)

    def get_spareparts(self):
        return self.filter(is_spareparts=True)

    def get_stockable(self):
        return self.filter(is_stockable=True)

    def can_be_purchased(self):
        return self.filter(can_be_purchased=True)

    def can_be_sold(self):
        return self.filter(can_be_sold=True)


class Product(SignalAwareClusterableModel,
              CreatorModelMixin,
              NumeratorMixin,
              KitBaseModel,
              PolymorphicModel):
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        permissions = (
            ('lock_product', 'Can lock Product'),
            ('unlock_product', 'Can unlock Product'),
            ('export_product', 'Can export Product'),
            ('import_product', 'Can import Product')
        )

    objects = ProductManager()

    picture = models.ForeignKey(
        Image, null=True, blank=True,
        on_delete=models.SET_NULL)
    category = TreeForeignKey(
        ProductCategory, null=True, blank=True,
        on_delete=models.PROTECT, verbose_name=_("Category"))
    barcode = models.CharField(
        max_length=125, null=True, blank=True,
        verbose_name=_("Barcode Number"))
    slug = models.SlugField(
        max_length=255,
        verbose_name=_('Slug'))
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'))
    description = RichTextField(
        null=True, blank=True,
        max_length=1000,
        verbose_name=_('Description'))
    suppliers = models.ManyToManyField(
        Supplier, blank=True,
        related_name='product_suppliers',
        help_text=_('Product supplier or vendors'))

    unit_price = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name=_('Unit price'))
    unit_of_measure = models.ForeignKey(
        UnitOfMeasure, on_delete=models.PROTECT,
        verbose_name=_('Unit'))
    minimum_stock = models.PositiveIntegerField(
        default=10, verbose_name=_("Min stock"))
    maximum_stock = models.PositiveIntegerField(
        default=1000, verbose_name=_("Max stock"))

    # Status
    # Inventories = stockable, consumable, active
    # Assets = stockable, not consumable, active
    # Service = not stockable, consumable, active

    is_locked = models.BooleanField(
        default=False, verbose_name=_("Locked"),
        help_text=_("Lock to prevent unwanted editing"))
    is_active = models.BooleanField(
        default=True, verbose_name=_("Active"),
        help_text=_("Deletion is not good, set to inactive instead"))
    is_consumable = models.BooleanField(
        default=True, verbose_name=_("Consumable"),
        help_text=_('This product is consumable'))
    is_stockable = models.BooleanField(
        default=True, verbose_name=_("Stockable"),
        help_text=_('This product is stockable eg. inventory or asset types'))
    is_bundle = models.BooleanField(
        default=False, verbose_name=_("Bundle"),
        help_text=_("This product's unit price and stock will ignored"))
    is_sparepart = models.BooleanField(
        default=False, verbose_name=_("Sparepart"),
        help_text=_('This product is sparepart item'))
    can_be_sold = models.BooleanField(
        default=False, verbose_name=_("Can be sold"))
    can_be_purchased = models.BooleanField(
        default=True, verbose_name=_("Can be purchased"))

    autocomplete_search_field = 'name'

    def autocomplete_label(self):
        return "{} ({})".format(self.name, self.inner_id)

    def __str__(self):
        return "{} ({})".format(self.name, self.inner_id)

    def natural_key(self):
        keys = (self.inner_id,)
        return keys

    def lock(self):
        self.is_locked = True
        self.save()

    def unlock(self):
        self.is_locked = False
        self.save()

    def get_counter(self):
        # Get ContentTypeCounter instance for this model
        poly = get_base_polymorphic_model(self.__class__)
        parent = None if self.__class__ == 'Product' else poly
        ct_counter = Numerator.get_instance(self, model=parent)
        return ct_counter

    def save(self, *args, **kwargs):
        self.slug = text.slugify(self.name)
        super().save(*args, **kwargs)


class Specification(Orderable, KitBaseModel):
    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")
        unique_together = ('product', 'feature')

    product = ParentalKey(
        Product, on_delete=models.CASCADE,
        related_name='product_specifications',
        verbose_name=_("Product"))
    feature = models.CharField(
        max_length=255, verbose_name=_("Feature"))
    value = models.CharField(
        max_length=255, verbose_name=_("Value"))
    note = models.CharField(
        null=True, blank=True,
        max_length=255, verbose_name=_("Note"))

    def __str__(self):
        return "{} ({})".format(self.product.name, self.feature.name)


class Inventory(Product):
    class Meta:
        verbose_name = _('Inventory')
        verbose_name_plural = _('Inventories')
        permissions = (
            ('lock_inventory', 'Can lock Inventory'),
            ('unlock_inventory', 'Can unlock Inventory'),
            ('export_inventory', 'Can export Inventory'),
            ('import_inventory', 'Can import Inventory')
        )

    doc_code = 'PRD.INV'

    def save(self, *args, **kwargs):
        self.is_stockable = True
        self.is_consumable = True
        super().save(*args, **kwargs)


class Asset(Product):
    class Meta:
        verbose_name = _('Asset')
        verbose_name_plural = _('Assets')
        permissions = (
            ('lock_asset', 'Can lock Asset'),
            ('unlock_asset', 'Can unlock Asset'),
            ('export_asset', 'Can export Asset'),
            ('import_asset', 'Can import Asset')
        )

    doc_code = 'PRD.ASS'

    def save(self, *args, **kwargs):
        self.is_stockable = True
        self.is_consumable = False
        super().save(*args, **kwargs)


class Service(Product):
    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        permissions = (
            ('lock_service', 'Can lock Service'),
            ('unlock_service', 'Can unlock Service'),
            ('export_service', 'Can export Service'),
            ('import_service', 'Can import Service')
        )

    doc_code = 'PRD.SRV'

    def save(self, *args, **kwargs):
        self.is_stockable = False
        self.is_consumable = False
        self.is_bundle = False
        self.is_sparepart = False
        super().save(*args, **kwargs)


class Bundle(Product):
    class Meta:
        verbose_name = _('Bundle')
        verbose_name_plural = _('Bundles')
        permissions = (
            ('lock_bundle', 'Can lock Bundle'),
            ('unlock_bundle', 'Can unlock Bundle'),
            ('export_bundle', 'Can export Bundle'),
            ('import_bundle', 'Can import Bundle')
        )

    doc_code = 'PRD.BND'

    def save(self, *args, **kwargs):
        self.is_stockable = False
        self.is_consumable = False
        self.is_bundle = True
        self.is_sparepart = False
        super().save(*args, **kwargs)


class Sparepart(Orderable, KitBaseModel):
    class Meta:
        verbose_name = _("Sparepart")
        verbose_name_plural = _("Spareparts")
        unique_together = ('product', 'sparepart')

    product = ParentalKey(
        Bundle, on_delete=models.CASCADE,
        related_name='spareparts',
        verbose_name=_("Product"))
    sparepart = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='product_spareparts',
        verbose_name=_("Sparepart"))
    quantity = models.PositiveIntegerField(
        default=1, verbose_name=_("Quantity"))

    def __str__(self):
        return self.product.name
