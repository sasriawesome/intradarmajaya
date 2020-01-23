from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtailkit.core.models import MAX_LEN_MEDIUM, MAX_LEN_SHORT, KitBaseModel


class Room(KitBaseModel):
    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')

    code = models.CharField(
        max_length=MAX_LEN_SHORT,
        verbose_name=_('Code'))
    name = models.CharField(
        max_length=MAX_LEN_SHORT,
        verbose_name=_('Name'))