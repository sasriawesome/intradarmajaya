from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from wagtail.contrib.settings.models import BaseSetting
from wagtail.images.models import Image
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList, FieldPanel, MultiFieldPanel, FieldRowPanel


class CompanySettings(BaseSetting):
    class Meta:
        verbose_name = _('Company')

    menu_icon = 'tag'

    fiscal_default = timezone.make_aware(
        timezone.datetime(timezone.now().year, 1, 1, 0, 0, 0 ))

    fiscal_year_start = models.DateField(
        default=fiscal_default, verbose_name=_('Fiscal year start'))
    fiscal_year_end = models.DateField(
        default=timezone.now, verbose_name=_('Fiscal year end'))

    logo = models.ForeignKey(
        Image, null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Logo'),
        help_text=_('Your company Logo (square, transparent baground is better)'))
    name = models.CharField(
        null=True, blank=True,
        max_length=255, help_text=_('Your company name'))
    tagline = models.CharField(
        null=True, blank=True,
        max_length=255, help_text=_('Your company tagline'))
    website = models.CharField(
        null=True, blank=True,
        max_length=255, help_text=_('Website URL.'))
    sitename = models.CharField(
        null=True, blank=True,
        max_length=255, help_text=_('Site name, widely used in this site.'))

    street1 = models.CharField(
        null=True, blank=True,
        max_length=255,
        verbose_name=_('Address 1'))
    street2 = models.CharField(
        null=True, blank=True,
        max_length=255,
        verbose_name=_('Address 2'))
    city = models.CharField(
        null=True, blank=True,
        max_length=255,
        verbose_name=_('City'))
    province = models.CharField(
        null=True, blank=True,
        max_length=255,
        verbose_name=_('Province'))
    country = models.CharField(
        null=True, blank=True,
        max_length=255,
        verbose_name=_('Country'))
    zipcode = models.CharField(
        null=True, blank=True,
        max_length=255,
        verbose_name=_('Zip Code'))

    phone = models.CharField(
        null=True, blank=True,
        max_length=255, help_text=_('Phone number @'))
    fax = models.CharField(
        null=True, blank=True,
        max_length=255, help_text=_('Fax number @'))
    email = models.EmailField(
        null=True, blank=True,
        max_length=255, help_text=_('Valid email'))
    facebook = models.URLField(
        null=True, blank=True,
        help_text=_('Facebook page URL'))
    twitter = models.CharField(
        null=True, blank=True,
        max_length=255, help_text=_('twitter username, without the @'))
    instagram = models.CharField(
        null=True, blank=True,
        max_length=255, help_text=_('Instagram username, without the @'))
    youtube = models.URLField(
        null=True, blank=True,
        help_text=_('YouTube channel or user account URL'))

    basic_panels = [
        MultiFieldPanel([
            ImageChooserPanel('logo'),
            FieldPanel('name'),
            FieldPanel('tagline'),
            FieldPanel('website'),
            FieldPanel('sitename'),
        ])
    ]

    address_panels = [
        MultiFieldPanel([
            FieldPanel('street1'),
            FieldPanel('street2'),
            FieldPanel('city'),
            FieldPanel('province'),
            FieldPanel('country'),
            FieldPanel('zipcode'),
        ])
    ]

    contact_panels = [
        MultiFieldPanel([
            FieldPanel('phone'),
            FieldPanel('fax'),
            FieldPanel('email'),
            FieldPanel('facebook'),
            FieldPanel('twitter'),
            FieldPanel('instagram'),
            FieldPanel('youtube'),
        ])
    ]

    misc_panels = [
        MultiFieldPanel([
            FieldPanel('fiscal_year_start'),
            FieldPanel('fiscal_year_end'),
        ])
    ]

    edit_handler = TabbedInterface([
        ObjectList(basic_panels, heading=_('Basic')),
        ObjectList(address_panels, heading=_('Address')),
        ObjectList(contact_panels, heading=_('Contact')),
        ObjectList(misc_panels, heading=_('Misc'))
    ])

    @property
    def full_address(self):
        line1 = []
        if self.street1:
            line1.append(self.street1)
        if self.street2:
            line1.append(self.street2)

        line2 = []
        if self.zipcode:
            line2.append(self.city)
        if self.province:
            line2.append(self.province)
        if self.country:
            line2.append(self.country)
        if self.zipcode:
            line2.append(self.zipcode)

        line1 = " ".join(line1)
        line2 = ", ".join(line2)
        return line1, line2
