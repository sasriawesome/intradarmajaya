import enum
from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.core.models import Orderable
from modelcluster.models import ClusterableModel, ParentalKey
from wagtailkit.core.models import KitBaseModel, MAX_LEN_MEDIUM
from wagtailkit.numerators.models import NumeratorMixin
from wagtailkit.students.models import Student
from wagtailkit.academic.models import AcademicYear
from wagtailkit.lectures.models import Lecture


class EnrollmentStatus(enum.Enum):
    TRASH = 'TRASH'  # student can't delete enrollment, move to trash instead
    DRAFT = 'DRAFT'  # student create new enrolment
    SUBMITTED = 'SUBMITTED'  # after student submit, and waiting for coach validation
    REVISION = 'REVISION'  # after coach request for revision
    VALID = 'VALID'  # after coach validate enrolment


class EnrollmentCriteria(enum.Enum):
    NEW = '1'
    REMEDY = '2'


class EnrollmentPlan(KitBaseModel):
    class Meta:
        verbose_name = _("Enrollment Plan")
        verbose_name_plural = _("Enrollment Plans")

    student = models.OneToOneField(
        Student, on_delete=models.CASCADE,
        verbose_name=_("Student"))
    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.CASCADE,
        verbose_name=_('Lecture'))
    criteria = models.CharField(
        max_length=2,
        choices=[(str(x.value), str(x.name)) for x in EnrollmentCriteria],
        default=EnrollmentCriteria.NEW,
        verbose_name=_('Criteria'))

    def __str__(self):
        return "{} {}".format(self.student, self.lecture.code)


class Enrollment(ClusterableModel, NumeratorMixin, KitBaseModel):
    class Meta:
        verbose_name = _("Enrollment")
        verbose_name_plural = _("Enrollments")

    doc_code = 'KRS'
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE,
        verbose_name=_("Student"))
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        verbose_name=_('Academic Year'))
    note = models.TextField(
        max_length=MAX_LEN_MEDIUM,
        null=True, blank=True,
        verbose_name=_("Note for coach"))
    coach_review = models.TextField(
        max_length=MAX_LEN_MEDIUM,
        null=True, blank=True,
        verbose_name=_("Coach review"))
    status = models.CharField(
        max_length=2,
        choices=[(str(x.value), str(x.name)) for x in EnrollmentStatus],
        default=EnrollmentStatus.DRAFT,
        verbose_name=_('Status'))

    def __str__(self):
        return self.doc_code


class EnrollmentItem(Orderable, KitBaseModel):
    class Meta:
        verbose_name = _("Enrollment Item")
        verbose_name_plural = _("Enrollment Items")
        unique_together = ('enrollment', 'lecture')

    enrollment = ParentalKey(
        Enrollment, related_name='lectures',
        on_delete=models.CASCADE,
        verbose_name=_('Enrolment'))
    lecture = ParentalKey(
        Lecture, related_name='enrollments',
        on_delete=models.CASCADE,
        verbose_name=_('Lecture'))
    criteria = models.CharField(
        max_length=2,
        choices=[(str(x.value), str(x.name)) for x in EnrollmentCriteria],
        default=EnrollmentCriteria.NEW,
        verbose_name=_('Criteria'))

    def __str__(self):
        return str(self.lecture)