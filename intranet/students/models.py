from django.db import models

from wagtailkit.lectures.models import Lecture, LectureSchedule, StudentScore


class LectureForStudent(Lecture):
    class Meta:
        proxy = True


class ScheduleForStudent(LectureSchedule):
    class Meta:
        proxy = True


class ScoreManager(models.Manager):
    pass


class ScoreForStudent(StudentScore):
    class Meta:
        proxy = True

    alt_manager = ScoreManager()
