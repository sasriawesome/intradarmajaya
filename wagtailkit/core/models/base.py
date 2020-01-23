import uuid
import json

from django.db import models
from django.utils import translation, timezone
from django.conf import settings

_ = translation.gettext_lazy


class KitBaseModel(models.Model):
    """ Base model with uuid primary key """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('ID'))
    date_created = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Date created'))
    date_modified = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Date modified'))

    class Meta:
        abstract = True
        ordering = ['-date_created']

    def save(self,
             force_insert=False,
             force_update=False,
             using=None,
             update_fields=None):
        # update when object modified
        self.date_modified = timezone.now()
        super().save(
            force_insert=force_insert, force_update=force_update,
            using=using, update_fields=update_fields
        )


class CreatorModelMixin(models.Model):
    class Meta:
        abstract = True

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.PROTECT,
        verbose_name=_('Creator')
    )

class MetaFieldMixin(models.Model):
    """ Add Metafield to model, Metafield save data in json string format """

    class Meta:
        abstract = True

    metafield = models.CharField(
        max_length=1000, null=True, blank=True,
        verbose_name=_('Metafield'))

    def get_metafield(self):
        metafield = self.metafield or "{}"
        return json.loads(metafield)

    @property
    def verbose_name(self):
        metafield = self.get_metafield()
        return metafield.get('verbose_name') or '-'

    def set_metafield(self):
        """  Implementation:
         self.metafield = json.dumps({
             'verbose_name': 'Object Your Verbose Name'
         })
        """
        raise NotImplementedError

    def save(self, *args, **kwargs):
        self.set_metafield()
        super().save(*args, **kwargs)