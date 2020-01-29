from django.db import models
from django.utils import translation
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

from mptt.models import TreeForeignKey
from wagtailkit.numerators.models import NumeratorMixin
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


class Student(NumeratorMixin, KitBaseModel):
    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')

    objects = StudentManager()

    inner_id = None
    sid = models.CharField(
        editable=False, unique=True, max_length=MAX_LEN_SHORT,
        verbose_name=_('Student ID'))
    person = models.OneToOneField(
        Person, on_delete=models.CASCADE,
        verbose_name=_("Person"))
    year_of_force = models.CharField(
        max_length=4,
        choices=[(str(x), str(x)) for x in range(2010, 2030)],
        default='2019',
        verbose_name=_("Year of force"))
    program_study = models.ForeignKey(
        ProgramStudy, on_delete=models.PROTECT,
        verbose_name=_('Program Study'))
    registration = models.CharField(
        max_length=2,
        choices=(('1','Reguler'), ('P', 'Transfer')),
        default='1',
        verbose_name=_("Registration"))
    is_active = models.BooleanField(
        default=False, verbose_name=_("Active status"))

    def generate_inner_id(self):
        """ Generate human friendly Student Number,
            override this method to customize inner_id format
            """
        form = [
            self.year_of_force[2:4],
            self.program_study.faculty.code,
            self.program_study.code,
            self.registration,
            str(self.reg_number).zfill(4)
        ]
        self.sid = ''.join(form)
        return self.sid

    def __str__(self):
        return self.person.fullname

    def natural_key(self):
        natural_key = (self.sid,)
        return natural_key
