import enum
from django.db import models
from django.utils import translation

from wagtailkit.core.models import KitBaseModel, MAX_LEN_LONG

from wagtailkit.teachers.models import Teacher
from wagtailkit.students.models import Student
from wagtailkit.lectures.models import LectureSchedule, LectureStudent

_ = translation.gettext_lazy


class AttendantStatus(enum.Enum):
    PRESENT = 'PR'
    SICK = 'SC'
    ABSENT = 'AB'
    PERMIT = 'PE'


class Holiday(KitBaseModel):
    class Meta:
        verbose_name = _("Holiday")
        verbose_name_plural = _("Holidays")

    date_start = models.DateField(
        verbose_name=_("Date start"))
    date_end = models.DateField(
        verbose_name=_("Date end"))
    name = models.CharField(
        max_length=MAX_LEN_LONG,
        verbose_name=_("Note"))
    note = models.TextField(
        null=True, blank=True,
        max_length=MAX_LEN_LONG,
        verbose_name=_("Description"))

    def __str__(self):
        return self.name


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

    student = models.ForeignKey(
        LectureStudent,
        on_delete=models.CASCADE,
        related_name='attendances',
        verbose_name=_("Student"))
    schedule = models.ForeignKey(
        LectureSchedule, on_delete=models.CASCADE,
        verbose_name=_("Schedule"))
    status = models.CharField(
        max_length=3, choices=[(str(x.value), str(x.name).title()) for x in AttendantStatus],
        default=AttendantStatus.PRESENT.value, verbose_name=_("Status"))
    note = models.CharField(
        max_length=MAX_LEN_LONG,
        null=True, blank=True,
        verbose_name=_("Note"))

    def __str__(self):
        return "{} {}".format(self.student, self.schedule)


class TeacherAttendance(KitBaseModel):
    class Meta:
        verbose_name = _("Teacher Attendance")
        verbose_name_plural = _("Teacher Attendances")
        unique_together = ('schedule', 'teacher')

    schedule = models.ForeignKey(
        LectureSchedule, on_delete=models.CASCADE,
        verbose_name=_("Schedule"))
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE,
        verbose_name=_("Teacher"))
    status = models.CharField(
        max_length=3, choices=[(str(x.value), str(x.name).title()) for x in AttendantStatus],
        default=AttendantStatus.PRESENT.value, verbose_name=_("Status"))
    note = models.CharField(
        max_length=MAX_LEN_LONG,
        null=True, blank=True,
        verbose_name=_("Note"))

    def __str__(self):
        return "{} {}".format(self.schedule)
