from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtailkit.core.models import KitBaseModel
from wagtailkit.numerators.models import NumeratorMixin
from wagtailkit.students.models import Student
from wagtailkit.lectures.models import Lecture


class Enrollment(NumeratorMixin, KitBaseModel):
    class Meta:
        verbose_name = _("Enrollment")
        verbose_name_plural = _("Enrollments")

    doc_code = 'KRS'
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE,
        verbose_name=_("Student"))

    def __str__(self):
        return self.doc_code


class EnrollmentItem(KitBaseModel):
    class Meta:
        verbose_name = _("Enrollment Item")
        verbose_name_plural = _("Enrollment Items")
        unique_together = ('enrollment', 'lecture')

    STATUS = (
        ('1','New'),
        ('2','Remedy'),
    )

    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        verbose_name=_('Enrolment'))
    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.CASCADE,
        verbose_name=_('Lecture'))
    status = models.CharField(
        max_length=2,
        default=1,
        choices=STATUS,
        verbose_name=_('Status'))

    def __str__(self):
        return str(self.lecture)
