from django.db import models
from django.utils import translation

from wagtailkit.core.models import KitBaseModel, MAX_LEN_LONG

from wagtailkit.teachers.models import Teacher
from wagtailkit.students.models import Student
from wagtailkit.lectures.models import LectureSchedule

_ = translation.gettext_lazy


class LectureAttendance(LectureSchedule):
    class Meta:
        proxy = True
        verbose_name = _("Lecture Attendance")
        verbose_name_plural = _("Lecture Attendances")


class StudentAttendance(KitBaseModel):
    class Meta:
        verbose_name = _("Student Attendance")
        verbose_name_plural = _("Student Attendances")
        unique_together = ('schedule', 'student')

    PRESENT = 'PR'
    SICK = 'SC'
    ABSENT = 'AB'
    PERMIT = 'PR'
    STATUS = (
        (PRESENT, _('Present')),
        (SICK, _('Sick')),
        (ABSENT, _('Absent')),
        (PERMIT, _('Permit')),
    )

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE,
        verbose_name=_("Student"))
    schedule = models.ForeignKey(
        LectureSchedule, on_delete=models.CASCADE,
        verbose_name=_("Schedule"))
    status = models.CharField(
        max_length=3, choices=STATUS,
        default=PRESENT, verbose_name=_("Status"))
    note = models.CharField(
        max_length=MAX_LEN_LONG,
        null=True, blank=True,
        verbose_name=_("Note"))


class TeacherAttendance(KitBaseModel):
    class Meta:
        verbose_name = _("Teacher Attendance")
        verbose_name_plural = _("Teacher Attendances")
        unique_together = ('schedule', 'teacher')

    PRESENT = 'PR'
    SICK = 'SC'
    ABSENT = 'AB'
    PERMIT = 'PR'
    STATUS = (
        (PRESENT, _('Present')),
        (SICK, _('Sict')),
        (ABSENT, _('Absent')),
        (PERMIT, _('Permit')),
    )

    schedule = models.ForeignKey(
        LectureSchedule, on_delete=models.CASCADE,
        verbose_name=_("Schedule"))
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE,
        verbose_name=_("Teacher"))
    status = models.CharField(
        max_length=3, choices=STATUS,
        default=PRESENT, verbose_name=_("Status"))
    note = models.CharField(
        max_length=MAX_LEN_LONG,
        null=True, blank=True,
        verbose_name=_("Note"))
