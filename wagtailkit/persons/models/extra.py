import uuid
from django.db import models
from django.utils import translation, text, timezone

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, ObjectList
from wagtail.snippets.models import register_snippet

from wagtailkit.core.models import (
    MAX_LEN_SHORT, MAX_LEN_MEDIUM, MAX_LEN_LONG,
    KitBaseModel)

_ = translation.gettext_lazy


@register_snippet
class EducationLevel(KitBaseModel):
    class Meta:
        verbose_name = _('Education Level')
        verbose_name_plural = _('Education Levels')

    slug = models.CharField(
        max_length=3, unique=True,
        verbose_name=_("Slug"))
    name = models.CharField(
        max_length=MAX_LEN_SHORT,
        verbose_name=_("Name"))
    description = models.TextField(
        max_length=MAX_LEN_MEDIUM,
        null=True, blank=True,
        verbose_name=_("Description"))

    edit_handler = ObjectList([
        MultiFieldPanel([
            FieldPanel('slug'),
            FieldPanel('name'),
            FieldPanel('description'),
        ])
    ])

    def __str__(self):
        self.slug = text.slugify(self.slug).upper()
        return self.name


class ContactInfo(models.Model):
    class Meta:
        abstract = True

    phone1 = models.CharField(
        max_length=MAX_LEN_SHORT,
        null=True, blank=True,
        verbose_name=_('Phone 1'))
    fax = models.CharField(
        max_length=MAX_LEN_SHORT,
        null=True, blank=True,
        verbose_name=_('Fax'))
    whatsapp = models.CharField(
        max_length=MAX_LEN_SHORT,
        null=True, blank=True,
        verbose_name=_('Whatsapp'))
    email = models.EmailField(
        max_length=MAX_LEN_SHORT,
        null=True, blank=True,
        verbose_name=_('Email'))
    website = models.CharField(
        max_length=MAX_LEN_SHORT,
        null=True, blank=True,
        verbose_name=_('Website'))


class Address(models.Model):
    class Meta:
        abstract = True

    street1 = models.CharField(
        null=True, blank=True,
        max_length=MAX_LEN_LONG,
        verbose_name=_('Address 1'))
    street2 = models.CharField(
        null=True, blank=True,
        max_length=MAX_LEN_LONG,
        verbose_name=_('Address 2'))
    city = models.CharField(
        null=True, blank=True,
        max_length=MAX_LEN_SHORT,
        verbose_name=_('City'))
    province = models.CharField(
        null=True, blank=True,
        max_length=MAX_LEN_SHORT,
        verbose_name=_('Province'))
    country = models.CharField(
        null=True, blank=True,
        max_length=MAX_LEN_SHORT,
        verbose_name=_('Country'))
    zipcode = models.CharField(
        null=True, blank=True,
        max_length=MAX_LEN_SHORT,
        verbose_name=_('Zip Code'))

    def __str__(self):
        return self.street1

    @property
    def fulladdress(self):
        address = [self.street1, self.street2, self.city,
                   self.province, self.country, self.zipcode]
        return ", ".join(address)
