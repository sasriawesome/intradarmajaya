from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.settings.models import BaseSetting
from wagtail.admin.edit_handlers import ObjectList, FieldPanel, MultiFieldPanel


class PersonSettings(BaseSetting):
    class Meta:
        verbose_name = _('Person Setting')
        verbose_name_plural = _('Person Settings')

    menu_icon = 'icon-group'

    show_histories_tab = models.BooleanField(
        default=True,
        verbose_name=_('Show histories tab'),
        help_text=_('Show formal person histories tab'))

    show_formal_education_history = models.BooleanField(
        default=True,
        verbose_name=_('Show formal education'),
        help_text=_('Show formal education histories panel'))

    show_nonformal_education_history = models.BooleanField(
        default=True,
        verbose_name=_('Show non formal education'),
        help_text=_('Show non formal education histories panel'))

    show_working_history = models.BooleanField(
        default=True,
        verbose_name=_('Show working experience'),
        help_text=_('Show working histories panel'))

    show_organization_history = models.BooleanField(
        default=True,
        verbose_name=_('Show organization experience'),
        help_text=_('Show organization histories panel'))

    show_skill = models.BooleanField(
        default=True,
        verbose_name=_('Show skill'),
        help_text=_('Show skills panel'))

    show_award = models.BooleanField(
        default=True,
        verbose_name=_('Show award'),
        help_text=_('Show awards panel'))

    show_publication = models.BooleanField(
        default=True,
        verbose_name=_('Show publication'),
        help_text=_('Show publications panel'))

    show_family = models.BooleanField(
        default=True,
        verbose_name=_('Show family tab'),
        help_text=_('Show family or relationship tab'))

    basic_panels = [
        MultiFieldPanel([
            FieldPanel('show_histories_tab'),
            FieldPanel('show_formal_education_history'),
            FieldPanel('show_nonformal_education_history'),
            FieldPanel('show_working_history'),
            FieldPanel('show_organization_history'),
            FieldPanel('show_skill'),
            FieldPanel('show_award'),
            FieldPanel('show_publication'),
            FieldPanel('show_family'),
        ])
    ]

    edit_handler = ObjectList(basic_panels)

    def __str__(self):
        return "{} {}".format(self.site, self._meta.verbose_name)