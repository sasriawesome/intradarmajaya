import uuid
import json

from django.db import models
from django.utils import translation, timezone
from django.conf import settings

from modelcluster.models import ClusterableModel, get_all_child_m2m_relations, get_all_child_relations

_ = translation.gettext_lazy


class SignalAwareClusterableModel(ClusterableModel):
    class Meta:
        abstract = True

    def save(self, commit_childs=True, **kwargs):
        """
        Save the model and commit all child relations.
        """
        child_relation_names = [rel.get_accessor_name() for rel in get_all_child_relations(self)]
        child_m2m_field_names = [field.name for field in get_all_child_m2m_relations(self)]

        update_fields = kwargs.pop('update_fields', None)
        if update_fields is None:
            real_update_fields = None
            relations_to_commit = child_relation_names
            m2m_fields_to_commit = child_m2m_field_names
        else:
            real_update_fields = []
            relations_to_commit = []
            m2m_fields_to_commit = []
            for field in update_fields:
                if field in child_relation_names:
                    relations_to_commit.append(field)
                elif field in child_m2m_field_names:
                    m2m_fields_to_commit.append(field)
                else:
                    real_update_fields.append(field)

        super(ClusterableModel, self).save(update_fields=real_update_fields, **kwargs)

        # Skip commit, when post_save using signal
        if commit_childs:
            for relation in relations_to_commit:
                getattr(self, relation).commit()

            for field in m2m_fields_to_commit:
                getattr(self, field).commit()


class KitBaseModel(models.Model):
    """ Base model with uuid primary key """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('ID'))
    date_created = models.DateTimeField(
        default=timezone.now,
        editable=False,
        verbose_name=_('Date created'))
    date_modified = models.DateTimeField(
        default=timezone.now,
        editable=False,
        verbose_name=_('Date modified'))
    is_deleted = models.BooleanField(default=False, editable=False)

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
        editable=False,
        null=True, blank=True,
        on_delete=models.PROTECT,
        verbose_name=_('Creator'))


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
