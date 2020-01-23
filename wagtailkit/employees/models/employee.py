import uuid
import json
from django.db import models
from django.utils import timezone, translation, text

from mptt.models import MPTTModel, TreeForeignKey

from wagtail.core.models import Orderable
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from wagtail.documents.models import Document
from modelcluster.models import ClusterableModel, ParentalKey

from wagtailkit.core.models import (
    MAX_LEN_SHORT, MAX_LEN_MEDIUM, MAX_LEN_LONG,
    CreatorModelMixin, MetaFieldMixin, KitBaseModel)
from wagtailkit.persons.models import Person

_ = translation.gettext_lazy


class DepartmentManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset().select_related('parent')
        return qs


class Department(CreatorModelMixin, MetaFieldMixin, MPTTModel, KitBaseModel):
    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')

    objects = DepartmentManager()

    parent = TreeForeignKey(
        'Department', null=True, blank=True,
        on_delete=models.PROTECT,
        related_name='department_upline',
        verbose_name=_('Upline'))
    slug = models.SlugField(
        unique=True,
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_('Slug'))
    name = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_('Name'))

    autocomplete_search_field = 'name'

    def autocomplete_label(self):
        return self.name

    def set_metafield(self):
        name = [self.name]
        parent = getattr(self, 'parent', None)
        if parent:
            name.append(parent.name)
        self.metafield = json.dumps({
            'verbose_name': ", ".join(name)
        })

    def __str__(self):
        return self.verbose_name

    def save(self, *args, **kwargs):
        self.slug = text.slugify(self.name)
        self.set_metafield()
        super().save(*args, **kwargs)


@register_snippet
class Employment(index.Indexed, KitBaseModel):
    class Meta:
        verbose_name = _('Employment')
        verbose_name_plural = _('Employments')

    slug = models.SlugField(
        unique=True, max_length=MAX_LEN_MEDIUM,
        verbose_name=_('Slug'))
    name = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_('Name'))
    note = models.TextField(
        null=True, blank=True,
        max_length=MAX_LEN_LONG,
        verbose_name=_('Note'))

    search_fields = [
        index.SearchField('name', partial_match=True)
    ]

    panels = [
        FieldPanel('name'),
        FieldPanel('note')
    ]

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None):
        self.slug = text.slugify(self.name)
        super(Employment, self).save(
            force_insert, force_update, using, update_fields)


class EmployeeManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('person', 'department')

    def get_by_natural_key(self, eid):
        return self.get(eid=eid)


class Employee(ClusterableModel, CreatorModelMixin, MetaFieldMixin, KitBaseModel):
    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')

    objects = EmployeeManager()

    person = models.OneToOneField(
        Person, on_delete=models.CASCADE,
        verbose_name=_("Person"))
    eid = models.CharField(
        unique=True,
        max_length=MAX_LEN_SHORT,
        verbose_name=_('Employee ID'))
    department = TreeForeignKey(
        Department,
        on_delete=models.PROTECT,
        verbose_name=_('Department'))
    employment = models.ForeignKey(
        Employment, null=True, blank=True,
        on_delete=models.PROTECT,
        verbose_name=_("Employment"))
    attachment = models.ForeignKey(
        Document, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name=_('Attachment'), help_text=_('Contract Document')
    )
    is_active = models.BooleanField(
        default=False, verbose_name=_("Active"))

    def set_metafield(self):
        name = [self.person.fullname]
        department = getattr(self, 'department', None)
        if department:
            name.append(department.name)
        self.metafield = json.dumps({
            'verbose_name': ", ".join(name),
            'person': name[0]
        })

    @property
    def primary_chair(self):
        primary_chair = self.chairs.filter(is_primary=True, is_active=True)
        active_chairs = self.chairs.filter(is_active=True)
        if primary_chair:
            return primary_chair[0]
        else:
            return None if not active_chairs else active_chairs[0]

    def __str__(self):
        return self.verbose_name

    def natural_key(self):
        natural_key = (self.eid,)
        return natural_key

    def save(self, *args, **kwargs):
        self.set_metafield()
        super().save(*args, **kwargs)


class PersonAsEmployeeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def get_employees(self):
        return super().get_queryset().filter(
            models.Q(employee__isnull=False))

    def get_by_natural_key(self, eid):
        return self.get(eid=eid)


class PersonAsEmployee(Person):
    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        proxy = True

    objects = PersonAsEmployeeManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
