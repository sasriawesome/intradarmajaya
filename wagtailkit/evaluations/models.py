from django.db import models
from django.utils import translation
from django.core.validators import MinValueValidator, MaxValueValidator

from wagtail.core.fields import RichTextField

from wagtailkit.core.models import (
    KitBaseModel, MAX_LEN_SHORT, MAX_LEN_LONG, MAX_RICHTEXT)

from wagtailkit.numerators.models import NumeratorMixin

_ = translation.gettext_lazy


class EvalQuestionGroup(KitBaseModel):
    class Meta:
        verbose_name = _("Eval Question Group")
        verbose_name_plural = _("Eval Question Groups")

    code = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1000)],
        verbose_name=_('code'))
    name = models.CharField(
        max_length=MAX_LEN_SHORT,
        verbose_name=_('Name'))
    description = RichTextField(
        max_length=MAX_RICHTEXT,
        null=True, blank=True,
        verbose_name=_("Description"))

    def __str__(self):
        return self.name


class EvalQuestion(KitBaseModel):
    class Meta:
        verbose_name = _("Eval Question")
        verbose_name_plural = _("Eval Questions")
        ordering = ['-date_created']

    group = models.ForeignKey(
        EvalQuestionGroup, on_delete=models.CASCADE,
        verbose_name=_('Question group'))
    question = RichTextField(
        max_length=MAX_RICHTEXT,
        verbose_name=_("Question"))

    def __str__(self):
        return self.question


class Evaluation(NumeratorMixin, KitBaseModel):
    class Meta:
        verbose_name = _("Evaluation")
        verbose_name_plural = _("Evaluations")

    doc_code = 'EVAL'

    title = models.CharField(
        max_length=MAX_LEN_LONG,
        verbose_name=_('Title'))
    questions = models.ManyToManyField(
        EvalQuestion, related_name='evaluations',
        verbose_name=_('Questions'))

    def __str__(self):
        return self.title