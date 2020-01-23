from .lecture import LectureSchedule, Lecture
from django.utils.translation import gettext_lazy as _


class LectureStudentAttendance(LectureSchedule):
    class Meta:
        verbose_name = _("Lecture Attendance")
        verbose_name_plural = _("Lecture Attendances")
        proxy = True


class LectureStudentScore(Lecture):
    class Meta:
        verbose_name = _("Lecture Student Score")
        verbose_name_plural = _("Lecture Student Scores")
        proxy = True
