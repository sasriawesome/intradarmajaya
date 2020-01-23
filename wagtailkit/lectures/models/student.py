from django.db import models
from django.utils import translation
from django.contrib.auth import get_user_model

from mptt.models import TreeForeignKey

from wagtailkit.core.models import KitBaseModel, MAX_LEN_SHORT, MAX_LEN_LONG
from wagtailkit.persons.models import Person
from wagtailkit.academic.models import ProgramStudy

_ = translation.gettext_lazy


class PersonAsStudent(Person):
    class Meta:
        verbose_name = _('Persons')
        verbose_name_plural = _('Persons')
        proxy = True

    def save(self, force_insert=False, force_update=False,
             using=None,
             update_fields=None):
        super().save(force_insert, force_update, using,
                     update_fields)


class StudentManager(models.Manager):

    def get_by_natural_key(self, sid):
        return self.get(sid=sid)


class Student(KitBaseModel):
    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')

    objects = StudentManager()
    person = models.OneToOneField(
        Person, on_delete=models.CASCADE,
        verbose_name=_("Person"))
    sid = models.CharField(
        unique=True, max_length=MAX_LEN_SHORT),
    program_study = TreeForeignKey(
        ProgramStudy, on_delete=models.PROTECT,
        verbose_name=_('Program Study'))
    is_active = models.BooleanField(
        default=False, verbose_name=_("Active status"))

    def __str__(self):
        return self.person.fullname

    def natural_key(self):
        natural_key = (self.sid,)
        return natural_key
