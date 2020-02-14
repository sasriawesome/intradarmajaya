from django.db import models
from django.db.models.signals import post_save
from django.utils import translation
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator

from wagtail.core.fields import RichTextField

from wagtailkit.core.models import (
    KitBaseModel, CreatorModelMixin, MAX_LEN_SHORT, MAX_LEN_LONG, MAX_RICHTEXT)
from wagtailkit.numerators.models import NumeratorMixin
from wagtailkit.students.models import Student
from wagtailkit.lectures.models import Lecture

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



class LectureEvaluation(NumeratorMixin, CreatorModelMixin, KitBaseModel):
    class Meta:
        verbose_name = _("Lecture Evaluation")
        verbose_name_plural = _("Lecture Evaluations")

    doc_code = 'LEV'

    lecture = models.ForeignKey(
        Lecture, on_delete=models.CASCADE,
        verbose_name=_("Lecture"))
    student = models.ForeignKey(
        Student, null=True, blank=False,
        on_delete=models.SET_NULL,
        verbose_name=_("Student"))
    evaluation = models.ForeignKey(
        Evaluation, on_delete=models.PROTECT,
        verbose_name=_('Evaluation'))

    @property
    def title(self):
        return "Evaluasi {} oleh {}".format(self.lecture, self.student)

    def __str__(self):
        return self.title


class LectureEvaluationScore(KitBaseModel):
    class Meta:
        verbose_name = _("Lecture Evaluation Score")
        verbose_name_plural = _("Lecture Evaluation Scores")
        ordering = ('question__group__code', 'question__date_created',)

    lecture_evaluation = models.ForeignKey(
        LectureEvaluation, on_delete=models.CASCADE,
        verbose_name=_("Lecture evaluation"))
    question = models.ForeignKey(
        EvalQuestion, on_delete=models.PROTECT,
        verbose_name=_("Question"))
    score = models.PositiveIntegerField(
        choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'),),
        help_text=_('1:Tidak Setuju > 5:Setuju'),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        default=3, verbose_name=_('Score'))

    @staticmethod
    @receiver(post_save, sender=LectureEvaluation)
    def create_evaluation_questions(sender, **kwargs):
        created = kwargs.pop('created', False)
        instance = kwargs.pop('instance', None)
        if created:
            questions = []
            for question in instance.evaluation.questions.all():
                lect_question = LectureEvaluationScore(
                    lecture_evaluation=instance,
                    question=question)
                questions.append(lect_question)
            LectureEvaluationScore.objects.bulk_create(questions)

    def __str__(self):
        return self.question.group.name
