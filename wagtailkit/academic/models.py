import uuid
from django.db import models, transaction
from django.utils import timezone, translation, text

from mptt.models import MPTTModel, TreeForeignKey

from wagtail.core.fields import RichTextField

from wagtailkit.core.models import (
    MAX_LEN_MEDIUM, MAX_LEN_LONG, MAX_RICHTEXT,
    KitBaseModel, CreatorModelMixin)
from wagtailkit.numerators.models import NumeratorMixin
from wagtailkit.persons.models import EducationLevel

_ = translation.gettext_lazy


class ResourceManagementUnit(CreatorModelMixin, MPTTModel, KitBaseModel):
    class Meta:
        verbose_name = _("Resource Management Unit")
        verbose_name_plural = _("Resource Management Unit")

    parent = TreeForeignKey(
        'academic.ResourceManagementUnit',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Parent'))
    code = models.SlugField(
        unique=True,
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Code"))
    name = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Name"))

    def __str__(self):
        return self.name


class ProgramStudy(KitBaseModel):
    class Meta:
        verbose_name = _("Program Study")
        verbose_name_plural = _("Program Studies")

    S1 = 'S1'
    S2 = 'S2'
    S3 = 'S3'
    LEVEL = (
        (S1, _('Bachelor')),
        (S2, _('Master')),
        (S3, _('Doctor')),
    )

    code = models.SlugField(
        unique=True,
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Code"))
    name = models.CharField(
        max_length=MAX_LEN_LONG,
        verbose_name=_("Name"))
    alias = models.CharField(
        null=True, blank=True,
        max_length=MAX_LEN_LONG,
        verbose_name=_("Alias"))
    rmu = TreeForeignKey(
        ResourceManagementUnit,
        on_delete=models.PROTECT,
        verbose_name=_("RMU"),
        help_text=_("Resource Management Unit"))
    level = models.CharField(
        max_length=3,
        choices=LEVEL,
        default=S1,
        verbose_name=_('Level'))
    description = RichTextField(
        null=True, blank=True,
        max_length=MAX_RICHTEXT,
        verbose_name=_("Description"))

    def __str__(self):
        return self.name


class SchoolYear(KitBaseModel):
    class Meta:
        verbose_name = _("School Year")
        verbose_name_plural = _("School Years")

    ODD = '1'
    EVEN = '2'
    SHORT = '3'
    SEMESTER = (
        (ODD, _('Odd')),
        (EVEN, _('Even')),
        (SHORT, _('Short')),
    )

    code = models.SlugField(
        unique=True,
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Code"))
    year = models.CharField(
        max_length=4,
        choices=[(str(x), str(x)) for x in range(2010, 2030)],
        default='2019',
        verbose_name=_("Year"))
    semester = models.CharField(
        max_length=2,
        choices=SEMESTER,
        default=ODD,
        verbose_name=_('Semester'))
    date_start = models.DateField(verbose_name=_("Date start"))
    date_end = models.DateField(verbose_name=_("Date end"))

    def __str__(self):
        return self.code


class Course(NumeratorMixin, KitBaseModel):
    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    MANDATORY = 'A'  # Wajib
    CHOICE = 'B'  # Pilihan
    INTEREST_MANDATORY = 'C'  # Wajibpeminatan
    INTEREST_CHOICE = 'D'  # Pilihan peminatan
    RESEARCH = 'S'  # Tugas akhir / Skripsi / Thesis / Disertasi
    COURSE_TYPE = (
        (MANDATORY, _('Mandatory')),
        (CHOICE, _('Choice')),
        (INTEREST_MANDATORY, _('Interest Mandatory')),
        (INTEREST_CHOICE, _('Interest Choice')),
        (RESEARCH, _('Research/Thesis/Disertation')),

    )

    MPK = 'A'
    MKK = 'B'
    MKB = 'C'
    MPB = 'D'
    MBB = 'E'
    MKDU = 'F'
    MKDK = 'G'
    COURSE_GROUP = (
        (MPK, _('MPK: Personal Development Course')),  # MPK(mata; kuliah; pengembangan; kepribadian)
        (MKK, _('MKK: Knowledge Foudation Course')),  # B = MKK(mata; kuliah; keilmuan; dan; keterampilan)
        (MKB, _('MKB: Creational Skill Course')),  # C = MKB(mata; kuliah; keahlian; berkarya)
        (MPB, _('MPB: Behavioral Skill Course')),  # D = MPB(mata; kuliah; perilaku; berkarya)
        (MBB, _('MBB: Life Skill Course')),  # E = MBB(mata; kuliah; berkehidupan; bermasyarakat)
        (MKDU, _('MKDU: Basic Knowledge Course')),  # F = MKU / MKDU(mata; kuliah; umum / mata; kuliah; dasar; umum)
        (MKDK, _('MKDK: Basic Skill Course')),  # G = MKDK(mata; kuliah; dasar; keahlian)
    )

    doc_code = "CRS"
    rmu = TreeForeignKey(
        ResourceManagementUnit,
        on_delete=models.PROTECT,
        verbose_name=_("RMU"),
        help_text=_("Resource Management Unit"))
    code = models.SlugField(
        unique=True,
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Code"))
    name = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Name"))
    teaching_method = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Teaching method"))
    equal_to = models.ForeignKey(
        "self", null=True, blank=True,
        on_delete=models.PROTECT,
        verbose_name=_("Equal to"))
    course_type = models.CharField(
        max_length=1,
        choices=COURSE_TYPE,
        default=MANDATORY,
        verbose_name=_("Course type"))
    course_group = models.CharField(
        max_length=4,
        choices=COURSE_GROUP,
        default=MPK,
        verbose_name=_("Course group"))
    description = RichTextField(
        null=True, blank=True,
        max_length=MAX_RICHTEXT,
        verbose_name=_("Description"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active status"))

    def __str__(self):
        return "{}, {}".format(self.inner_id, self.name)

    def get_requisite(self):
        return self.course_courseprerequisite.all()

    @property
    def prerequisite(self):
        req = ", ".join([str(i.requisite.name) for i in self.get_requisite()])
        return req


class CoursePreRequisite(KitBaseModel):
    class Meta:
        verbose_name = _("Course Pre Requisite")
        verbose_name_plural = _("Course Pre Requisite")

    course = models.ForeignKey(
        Course,
        related_name="course_prerequisites",
        on_delete=models.PROTECT,
        verbose_name=_("Course"))
    requisite = models.ForeignKey(
        Course, null=True, blank=True,
        related_name="prerequisites",
        on_delete=models.PROTECT, verbose_name=_("Requisite"))

    def __str__(self):
        return ", ".join([str(self.course.name), str(self.requisite.name)])


class CurriculumManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset().select_related('prodi')
        return qs

    def get_detail_sks(self):
        return self.get_queryset().prefetch_related('curriculumcourse_set').annotate(
            sks_mandatory=models.Sum('curriculumcourse__sks', filter=models.Q(
                curriculumcourse__course__course_type=Course.MANDATORY)),
            sks_choice=models.Sum('curriculumcourse__sks', filter=models.Q(
                curriculumcourse__course__course_type=Course.CHOICE)),
            sks_interest_mandatory=models.Sum('curriculumcourse__sks', filter=models.Q(
                curriculumcourse__course__course_type=Course.INTEREST_MANDATORY)),
            sks_interest_choice=models.Sum('curriculumcourse__sks', filter=models.Q(
                curriculumcourse__course__course_type=Course.INTEREST_CHOICE)),
            sks_research=models.Sum('curriculumcourse__sks', filter=models.Q(
                curriculumcourse__course__course_type=Course.INTEREST_CHOICE)),
        )


class Curriculum(KitBaseModel):
    class Meta:
        verbose_name = _("Curriculum")
        verbose_name_plural = _("Curriculums")

    objects = CurriculumManager()

    code = models.SlugField(
        unique=True,
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Code"))
    rmu = TreeForeignKey(
        ResourceManagementUnit,
        on_delete=models.PROTECT,
        verbose_name=_("RMU"),
        help_text=_("Resource Management Unit"))
    prodi = models.ForeignKey(
        ProgramStudy,
        on_delete=models.PROTECT,
        verbose_name=_("Program Study"))
    name = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Name"))
    sks_graduate = models.PositiveIntegerField(
        default=0,
        verbose_name=_("SKS graduate"))

    # TODO : create computed property for every Course.COURSE_TYPE

    def __str__(self):
        return self.name


class CurriculumCourse(NumeratorMixin, KitBaseModel):
    class Meta:
        verbose_name = _("Curricullum Course")
        verbose_name_plural = _("Curricullum Courses")

    MEETING = 'M'
    PRACTICE = 'P'
    FIELD_PRACTICE = 'F'
    SIMULATION = 'S'
    SKS_TYPE = (
        (MEETING, _('Meeting')),
        (PRACTICE, _('Practice')),
        (FIELD_PRACTICE, _('Field Practice')),
        (SIMULATION, _('Simulation'))
    )

    doc_code = "CRC.CI"

    curricullum = models.ForeignKey(
        Curriculum,
        on_delete=models.CASCADE,
        verbose_name=_("Curriculum"))
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name=_("Course"))
    sks = models.PositiveIntegerField(
        default=0, verbose_name=_("SKS"))
    sks_type = models.CharField(
        max_length=1,
        choices=SKS_TYPE,
        default=MEETING,
        verbose_name=_('SKS type'))

    def __str__(self):
        return "{} ({})".format(self.inner_id, self.course)
