import uuid
import json
from django.core import checks
from django.db import models, transaction
from django.utils import timezone, translation, text

from mptt.models import MPTTModel, TreeForeignKey

from wagtail.core.models import Orderable
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from wagtail.documents.models import Document
from modelcluster.models import ParentalKey

from wagtailkit.core.models import (
    MAX_LEN_SHORT, MAX_LEN_MEDIUM, MAX_LEN_LONG, MAX_RICHTEXT,
    CreatorModelMixin, MetaFieldMixin, KitBaseModel)

# Support InlinePanel In WagtailAdmin
from .employee import Employee, Department

_ = translation.gettext_lazy


class ChairManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset().select_related('department')
        return qs.prefetch_related('chairman_set')


class Chair(MetaFieldMixin, MPTTModel):
    class Meta:
        verbose_name = _('Chair')
        verbose_name_plural = _('Chairs')

    objects = ChairManager()

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4,
        editable=False, verbose_name=_('UUID'))
    slug = models.SlugField(
        unique=True,
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_('Slug'))
    parent = TreeForeignKey(
        'Chair', null=True, blank=True,
        on_delete=models.PROTECT,
        related_name='chair_upline',
        verbose_name=_('Upline')
    )
    position = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_('position'))
    department = TreeForeignKey(
        Department,
        on_delete=models.PROTECT,
        verbose_name=_('Department'))
    is_single = models.BooleanField(
        default=True, verbose_name=_('Single chair'))
    employee_required = models.IntegerField(
        default=1, verbose_name=_('Employee required'))
    description = models.TextField(
        null=True, blank=True,
        max_length=MAX_RICHTEXT,
        verbose_name=_('Description of Duty'))
    attachment = models.ForeignKey(
        Document, null=True, blank=True,
        on_delete=models.SET_NULL)

    def set_metafield(self):
        name = [self.position]
        department = getattr(self, 'department', None)
        if department:
            name.append(department.name)
        self.metafield = json.dumps({
            'verbose_name': ", ".join(name)
        })

    def get_chairman(self):
        qs = self.chairman_set.filter(is_active=True)
        return qs[:1] if self.is_single and bool(qs) else qs

    def chairman(self):
        return ", ".join([str(x) for x in self.get_chairman()]) or None

    def __str__(self):
        return self.verbose_name

    def save(self, *args, **kwargs):
        self.slug = text.slugify(self.position)
        self.set_metafield()
        super().save(*args, **kwargs)


class ChairmanManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('chair', 'employee')


class Chairman(Orderable, CreatorModelMixin, MetaFieldMixin, KitBaseModel):
    class Meta:
        verbose_name = _('Chairman')
        verbose_name_plural = _('Chairmans')
        unique_together = ('employee', 'chair')

    objects = ChairmanManager()

    chair = TreeForeignKey(
        Chair, on_delete=models.CASCADE,
        verbose_name=_("Chair"))
    employee = ParentalKey(
        Employee, on_delete=models.CASCADE,
        related_name='chairs',
        verbose_name=_("Employee"))
    is_primary = models.BooleanField(
        default=True, verbose_name=_("Primary"))
    is_active = models.BooleanField(
        default=False, verbose_name=_("Active"))
    attachment = models.ForeignKey(
        Document, null=True, blank=True,
        on_delete=models.SET_NULL)

    def set_metafield(self):
        name = (str(self.employee.person), str(self.chair))
        self.metafield = json.dumps({
            'verbose_name': "{} ({})".format(*name)
        })

    def __str__(self):
        return self.verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.set_metafield()
        self.creator = self.employee.creator
        super().save(
            force_insert, force_update, using, update_fields)
