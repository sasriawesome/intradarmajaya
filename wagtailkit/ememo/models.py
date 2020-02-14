from django.db import models
from django.utils import translation
from wagtail.core.fields import RichTextField
from wagtail.documents.models import Document
from wagtailkit.core.models import (
    MAX_LEN_LONG, MAX_RICHTEXT, KitBaseModel, CreatorModelMixin)
from wagtailkit.employees.models import Chairman
from wagtailkit.numerators.models import NumeratorMixin

_ = translation.gettext_lazy


class Memo(NumeratorMixin, CreatorModelMixin, KitBaseModel):
    class Meta:
        verbose_name = _("Memo")
        verbose_name_plural = _("Memos")

    doc_code = 'IM'

    receiver = models.ManyToManyField(
        Chairman,
        related_name='memos_received',
        verbose_name=_("Receiver"))
    cc = models.ManyToManyField(
        Chairman,
        related_name='cc',
        verbose_name=_("CC"))
    title = models.CharField(
        max_length=MAX_LEN_LONG,
        verbose_name=_("Title"))
    body = RichTextField(
        max_length=MAX_RICHTEXT,
        verbose_name=_("Body"))
    attachment = models.ForeignKey(
        Document, null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Attachment'))

    def __str__(self):
        return self.title

# class DispositionText(CreatorModelMixin, KitBaseModel):
#     class Meta:
#         verbose_name = _("Disposition Text")
#         verbose_name_plural = _("Disposition Texts")
#
#     text = models.CharField(
#         max_length=MAX_LEN_LONG,
#         verbose_name=_("text"))
#
#
# class Disposition(CreatorModelMixin, KitBaseModel):
#     class Meta:
#         verbose_name = _("Disposition")
#         verbose_name_plural = _("Dispositions")
#
#     memo = models.ForeignKey(
#         Memo, on_delete=models.CASCADE,
#         verbose_name=_('Memo'))
#     assign_to = models.ManyToManyField(
#         Chairman, related_name='memos_assigned',
#         verbose_name=_("Assign to"))
