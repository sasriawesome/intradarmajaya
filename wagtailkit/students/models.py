from django.db import models
from django.utils import translation
from django.core.validators import MinValueValidator, MaxValueValidator
from polymorphic.models import PolymorphicModel, PolymorphicManager

from wagtailkit.numerators.models import NumeratorMixin, Numerator
from wagtailkit.core.models import KitBaseModel, MAX_LEN_SHORT, MAX_LEN_MEDIUM
from wagtailkit.persons.models import Person, PersonManager
from wagtailkit.academic.models import ProgramStudy, SchoolYear, CurriculumCourse


_ = translation.gettext_lazy


class StudentPersonalManager(PersonManager):
    def get_queryset(self):
        return super().get_queryset().filter(
            models.Q(student__isnull=False) | models.Q(is_matriculant=True)
        ).prefetch_related('student')


class StudentPersonal(Person):
    class Meta:
        verbose_name = _('Student Personal')
        verbose_name_plural = _('Student Personals')
        proxy = True

    objects = StudentPersonalManager()

    @property
    def is_student(self):
        return bool(getattr(self, 'student', False))

    def save(self, *args, **kwargs):
        self.is_matriculant = True
        super().save(*args, **kwargs)


class StudentManager(models.Manager):
    def get_by_natural_key(self, sid):
        return self.get(sid=sid)


class Student(NumeratorMixin, KitBaseModel):
    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')
        permissions = (
            ('register_student', _('Can Register New Student')),
        )

    ACTIVE = 'ACT'
    ALUMNI = 'ALM'
    DROP_OUT = 'DRO'
    MOVED = 'MVD'
    MISC = 'MSC'
    STATUS = (
        (ACTIVE, _('Active')),
        (ALUMNI, _('Alumni')),
        (DROP_OUT, _('Drop out')),
        (MOVED, _('Moved')),
        (MISC, _('Misc')),
    )

    objects = StudentManager()

    inner_id = None
    numbering = Numerator.FIXED

    sid = models.CharField(
        editable=False, unique=True,
        max_length=MAX_LEN_SHORT,
        verbose_name=_('Student ID'))
    person = models.OneToOneField(
        Person, on_delete=models.CASCADE,
        verbose_name=_("Person"))
    year_of_force = models.ForeignKey(
        SchoolYear, on_delete=models.PROTECT,
        verbose_name=_("Year of force"))
    rmu = models.ForeignKey(
        ProgramStudy, on_delete=models.PROTECT,
        verbose_name=_('Program Study'))
    registration_id = models.CharField(
        max_length=MAX_LEN_SHORT,
        verbose_name=_("Registration ID"))
    registration = models.CharField(
        max_length=2, default='1',
        choices=(('1', 'Reguler'), ('P', 'Transfer')),
        verbose_name=_("Registration"))
    status = models.CharField(
        choices=STATUS, default=ACTIVE,
        max_length=MAX_LEN_SHORT,
        verbose_name=_('Status'))
    status_note = models.CharField(
        null=True, blank=True,
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_('Status note'))

    # wagtail autocomplete
    autocomplete_search_field = 'person__fullname'

    def autocomplete_label(self):
        return "{} | {}".format(self.sid, self.name())

    def generate_inner_id(self):
        """ Generate human friendly Student Number,
            override this method to customize inner_id format
            """
        form = [
            str(self.year_of_force.year_start)[2:4],
            self.rmu.number,
            self.registration,
            str(self.reg_number).zfill(4)
        ]
        self.sid = ''.join(form)
        return self.sid

    def get_counter(self):
        custom_code = self.get_custom_code()
        ct_counter = Numerator.get_instance(self, custom_code=custom_code)
        return ct_counter

    def get_custom_code(self):
        form = [
            str(self.year_of_force.year_start)[2:4],
            self.rmu.number,
            self.registration
        ]
        return '{}{}{}'.format(*form)

    def __str__(self):
        return self.person.fullname

    def name(self):
        return self.person.fullname

    def natural_key(self):
        natural_key = (self.sid,)
        return natural_key


class StudentScoreManager(PolymorphicManager):

    def get_queryset(self):
        return super().get_queryset().select_related(
            'student', 'course'
        ).annotate(
            sid = models.F('student__sid'),
            cid = models.F('course__course__inner_id'),
            curriculum = models.F('course__curriculum__code')
        )

class StudentScore(PolymorphicModel, KitBaseModel):
    class Meta:
        verbose_name = _("Student Score")
        verbose_name_plural = _("Student Scores")

    objects = StudentScoreManager()

    course = models.ForeignKey(
        CurriculumCourse,
        on_delete=models.PROTECT,
        related_name='student_scores',
        verbose_name=_('Course'))
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE,
        related_name='scores',
        verbose_name=_("Student"))
    numeric = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        verbose_name=_("Numeric Score"))
    alphabetic = models.CharField(
        max_length=1,
        verbose_name=_("Alphabetic Score"))

    def __str__(self):
        return "{} | {}".format(self.student, self.course)


class ConversionScore(StudentScore):
    class Meta:
        verbose_name = _("Conversion Score")
        verbose_name_plural = _("Conversion Scores")

    ori_code = models.CharField(
        max_length=MAX_LEN_SHORT,
        verbose_name=_('Origin Code'))
    ori_name = models.CharField(
        max_length=MAX_LEN_SHORT,
        verbose_name=_('Origin Name'))
    ori_numeric_score = models.DecimalField(
        default=1,
        max_digits=3,
        decimal_places=2,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(4),
        ],
        verbose_name=_('Origin Numeric'))
    ori_alphabetic_score = models.CharField(
        max_length=MAX_LEN_SHORT,
        verbose_name=_('Origin Alphabetic'))
