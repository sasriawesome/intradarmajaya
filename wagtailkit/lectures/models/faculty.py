from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import translation

from mptt.models import TreeForeignKey

from wagtailkit.core.models import KitBaseModel, CreatorModelMixin, MAX_LEN_SHORT
from wagtailkit.numerators.models import NumeratorMixin
from wagtailkit.core.utils.datetime import add_time
from wagtailkit.persons.models import Person
from wagtailkit.academic.models import CurriculumCourse, SchoolYear, ProgramStudy

_ = translation.gettext_lazy


class PersonAsFaculty(Person):
    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        proxy = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class FacultyManager(models.Manager):

    def get_by_natural_key(self, lid):
        return self.get(lid=lid)


class Faculty(CreatorModelMixin, KitBaseModel):
    class Meta:
        verbose_name = _('Teacher')
        verbose_name_plural = _('Teachers')

    objects = FacultyManager()
    person = models.OneToOneField(
        Person, on_delete=models.CASCADE,
        verbose_name=_("Person"))
    fid = models.CharField(
        unique=True, max_length=MAX_LEN_SHORT,
        verbose_name=_('Teacher ID'))
    is_nidn = models.BooleanField(
        default=False, verbose_name=_("ID is NIDN"))
    homebase = TreeForeignKey(
        ProgramStudy, on_delete=models.PROTECT,
        verbose_name=_('Homebase'))
    courses = models.ManyToManyField(
        CurriculumCourse, verbose_name=_('Courses'))
    is_active = models.BooleanField(
        default=False, verbose_name=_("Active status"))

    def __str__(self):
        return self.person.fullname

    @property
    def name(self):
        return self.person.fullname

    def natural_key(self):
        natural_key = (self.fid,)
        return natural_key


# class TeacherCourse(CreatorModelMixin, KitBaseModel):
#     class Meta:
#         verbose_name = _('Teacher course')
#         verbose_name_plural = _('Teacher Courses')
#

    # is_active = models.BooleanField(
    #     default=True, verbose_name=_("Active status"))
#
#     def clean(self):
#         assistant = getattr(self, 'assistant', None)
#         if self.teacher == assistant:
#             raise ValidationError(
#                 {"assistant": "Please select correct assistant."})
#
#     def __str__(self):
#         return ", ".join(
#             [str(self.teacher), str(self.curriculum_course)])
