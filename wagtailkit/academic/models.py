import uuid
from datetime import datetime
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


class Faculty(KitBaseModel):
    class Meta:
        verbose_name = _("Faculty")
        verbose_name_plural = _("Faculties")

    code = models.CharField(
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

    def __str__(self):
        return "{} ({})".format(self.name, self.alias)


class ProgramStudy(KitBaseModel):
    class Meta:
        verbose_name = _("Program Study")
        verbose_name_plural = _("Program Studies")

    S1 = '1'
    S2 = '2'
    D3 = '3'
    S3 = '4'
    LEVEL = (
        (D3, _('D3')),
        (S1, _('S1')),
        (S2, _('S2')),
        (S3, _('S3')),
    )

    code = models.CharField(
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
    level = models.CharField(
        max_length=3,
        choices=LEVEL,
        default=S1,
        verbose_name=_('Level'))
    rmu = TreeForeignKey(
        ResourceManagementUnit,
        on_delete=models.PROTECT,
        verbose_name=_("RMU"),
        help_text=_("Resource Management Unit"))
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.PROTECT,
        verbose_name=_("Faculty"))
    description = RichTextField(
        null=True, blank=True,
        max_length=MAX_RICHTEXT,
        verbose_name=_("Description"))

    def __str__(self):
        return "{} ({})".format(self.name, self.alias)


class SchoolYear(KitBaseModel):
    class Meta:
        verbose_name = _("School Year")
        verbose_name_plural = _("School Years")

    code = models.CharField(
        unique=True, editable=False,
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Code"))
    year_start = models.IntegerField(
        choices=[(x, str(x)) for x in range(2010, 2050)],
        default=2019,
        verbose_name=_("Year Start"))
    year_end = models.IntegerField(
        choices=[(x, str(x)) for x in range(2010, 2050)],
        default=2020,
        verbose_name=_("Year End"))

    def create_code(self):
        return "{}/{}".format(self.year_start, self.year_end)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        self.code = self.create_code()
        super().save(*args, **kwargs)


class AcademicYear(KitBaseModel):
    class Meta:
        verbose_name = _("Academic Year")
        verbose_name_plural = _("Academic Years")

    ODD = '1'
    EVEN = '2'
    SHORT = 'P'
    SEMESTER = (
        (ODD, _('Odd')),
        (EVEN, _('Even')),
        (SHORT, _('Short')),
    )

    code = models.CharField(
        unique=True, editable=False,
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Code"))
    school_year = models.ForeignKey(
        SchoolYear, on_delete=models.PROTECT,
        verbose_name=_("School year"))
    semester = models.CharField(
        max_length=2,
        choices=SEMESTER,
        default=ODD,
        verbose_name=_('Semester'))
    date_start = models.DateField(verbose_name=_("Date start"))
    date_end = models.DateField(verbose_name=_("Date end"))

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        self.code = "{} S{}".format(self.school_year, self.semester)
        super().save(*args, **kwargs)


class AcademicActivity(KitBaseModel):
    class Meta:
        verbose_name = _("Academic Activity")
        verbose_name_plural = _("Academic Activities")
        ordering = ('-date_start',)

    PENDING = 'PND'
    ONGOING = 'ONG'
    END = 'END'
    STATUS = (
        (PENDING, _('Pending')),
        (ONGOING, _('On Going')),
        (END, _('End')),
    )

    academic_year = models.ForeignKey(
        AcademicYear, on_delete=models.PROTECT,
        verbose_name=_('Academic Year'))
    date_start = models.DateField(verbose_name=_("Date start"))
    date_end = models.DateField(verbose_name=_("Date end"))
    activity = RichTextField(verbose_name=_("Activity"))
    rmu = TreeForeignKey(
        ResourceManagementUnit,
        on_delete=models.PROTECT,
        verbose_name=_("RMU"),
        help_text=_("Resource Management Unit"))

    def __str__(self):
        return "{} ({}/{})".format(
            self.academic_year,
            self.date_start.strftime('%d%m%Y'),
            self.date_end.strftime('%d%m%Y'),
        )

    @property
    def status(self):
        list_date_start = (self.date_start.year, self.date_start.month, self.date_start.day)
        list_date_end = (self.date_end.year, self.date_end.month, self.date_end.day)
        activity_date_start = timezone.make_aware(timezone.datetime(*list_date_start))
        activity_date_end = timezone.make_aware(timezone.datetime(*list_date_end, hour=23, minute=59, second=59))

        cond1 = activity_date_start > timezone.make_aware(datetime.now())
        cond2 = activity_date_start <= timezone.make_aware(datetime.now()) <= activity_date_end
        cond3 = timezone.make_aware(datetime.now()) > activity_date_end

        print("{} {} {}".format(activity_date_start, datetime.now(), activity_date_end))
        if cond1:
            return AcademicActivity.STATUS[0][1]
        if cond2:
            return AcademicActivity.STATUS[1][1]
        if cond3:
            return AcademicActivity.STATUS[2][1]
        else:
            return 'Not Defined'

class CourseType(KitBaseModel):
    """
        Jenis Mata Kuliah
        A : Wajib
        B : Pilihan
        C : Wajibpeminatan
        D : Pilihan peminatan
        S : Tugas akhir / Skripsi / Thesis / Disertasi
    """

    class Meta:
        verbose_name = _("Course Type")
        verbose_name_plural = _("Course Types")

    code = models.CharField(
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

    def __str__(self):
        return self.name


class CourseGroup(KitBaseModel):
    """
        Kelompok mata kuliah
        A: MPK : mata; kuliah; pengembangan; kepribadian
        B: MKK : mata; kuliah; keilmuan; dan; keterampilan
        C: MKB : mata; kuliah; keahlian; berkarya
        D: MPB : mata; kuliah; perilaku; berkarya
        E: MBB : mata; kuliah; berkehidupan; bermasyarakat
        F: MKDU : mata; kuliah; umum / mata; kuliah; dasar; umum
        G: MKDK : mata; kuliah; dasar; keahlian
    """

    class Meta:
        verbose_name = _("Course Group")
        verbose_name_plural = _("Course Groups")

    code = models.CharField(
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

    def __str__(self):
        return self.name


class Course(KitBaseModel):
    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    code = models.SlugField(
        unique=True,
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Code"))
    rmu = TreeForeignKey(
        ResourceManagementUnit,
        on_delete=models.PROTECT,
        verbose_name=_("RMU"),
        help_text=_("Resource Management Unit"))
    name = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Name"))
    teaching_method = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Teaching method"))
    course_type = models.ForeignKey(
        CourseType,
        on_delete=models.PROTECT,
        verbose_name=_("Course type"))
    course_group = models.ForeignKey(
        CourseGroup,
        on_delete=models.PROTECT,
        verbose_name=_("Course group"))
    equal_to = models.ForeignKey(
        "self", null=True, blank=True,
        on_delete=models.PROTECT,
        verbose_name=_("Equal to"))
    description = RichTextField(
        null=True, blank=True,
        max_length=MAX_RICHTEXT,
        verbose_name=_("Description"))
    has_syllabus = models.BooleanField(
        default=True, verbose_name=_("Has syllabus"))
    has_lpu = models.BooleanField(
        default=True, verbose_name=_("Has LPU"),
        help_text=_('Lecture Program Unit a.k.a SAP'))
    has_dictate = models.BooleanField(
        default=True, verbose_name=_("Has dictate"))
    has_teaching_material = models.BooleanField(
        default=True, verbose_name=_("Has teaching material"))
    has_practice_program = models.BooleanField(
        default=True, verbose_name=_("Has practice program"))
    is_active = models.BooleanField(
        default=True, verbose_name=_("Active status"))

    def __str__(self):
        return "{}, {}".format(self.code, self.name)

    def get_requisite(self):
        prerequesite = getattr(self, 'course_courseprerequisite', None)
        return [] if not prerequesite else prerequesite.all()

    @property
    def prerequisite(self):
        req = ", ".join([str(i.requisite.name) for i in self.get_requisite()])
        return req


# Todo Padanan
# class CourseEquality(KitBaseModel):
#
#     equal_to = models.ForeignKey(
#         "self", null=True, blank=True,
#         on_delete=models.PROTECT,
#         verbose_name=_("Equal to"))


class CoursePreRequisite(KitBaseModel):
    class Meta:
        verbose_name = _("Course Pre Requisite")
        verbose_name_plural = _("Course Pre Requisite")

    SCORE = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
    )
    course = models.ForeignKey(
        Course,
        related_name="course_prerequisites",
        on_delete=models.PROTECT,
        verbose_name=_("Course"))
    requisite = models.ForeignKey(
        Course, null=True, blank=True,
        related_name="prerequisites",
        on_delete=models.PROTECT, verbose_name=_("Requisite"))
    score = models.CharField(
        max_length=2, default='C',
        choices=SCORE,
        verbose_name=_('Min Graduated Score'))

    def __str__(self):
        return ", ".join([str(self.course.name), str(self.requisite.name)])


class CurriculumManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset().select_related('prodi')
        return qs

        # Todo Next
        # def get_detail_sks(self):
        #     return self.get_queryset().prefetch_related('curriculumcourse_set').annotate(
        #         sks_mandatory=models.Sum('curriculumcourse__sks', filter=models.Q(
        #             curriculumcourse__course__course_type=Course.MANDATORY)),
        #         sks_choice=models.Sum('curriculumcourse__sks', filter=models.Q(
        #             curriculumcourse__course__course_type=Course.CHOICE)),
        #         sks_interest_mandatory=models.Sum('curriculumcourse__sks', filter=models.Q(
        #             curriculumcourse__course__course_type=Course.INTEREST_MANDATORY)),
        #         sks_interest_choice=models.Sum('curriculumcourse__sks', filter=models.Q(
        #             curriculumcourse__course__course_type=Course.INTEREST_CHOICE)),
        #         sks_research=models.Sum('curriculumcourse__sks', filter=models.Q(
        #             curriculumcourse__course__course_type=Course.INTEREST_CHOICE)),
        #     )


class Curriculum(KitBaseModel):
    class Meta:
        verbose_name = _("Curriculum")
        verbose_name_plural = _("Curriculums")

    objects = CurriculumManager()

    code = models.CharField(
        unique=True,
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Code"))
    year = models.CharField(
        max_length=4,
        choices=[(str(x), str(x)) for x in range(2010, 2030)],
        default='2019',
        verbose_name=_("Year"))
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

    def create_code(self):
        self.code = "".join([self.prodi.alias, self.year])

    def save(self, *args, **kwargs):
        self.create_code()
        super(Curriculum, self).save(*args, **kwargs)


class CurricullumCourseManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().annotate(
            course_code = models.F('course__code'),
            course_name = models.F('course__name'),
        )


class CurriculumCourse(KitBaseModel):
    class Meta:
        verbose_name = _("Curricullum Course")
        verbose_name_plural = _("Curricullum Courses")
        unique_together = ('curricullum', 'course')

    SEMESTER = (
        ('1', _('Odd')),
        ('2', _('Even')),
    )

    objects = CurricullumCourseManager()

    curricullum = models.ForeignKey(
        Curriculum,
        on_delete=models.CASCADE,
        verbose_name=_("Curriculum"))
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name=_("Course"))
    semester_number = models.CharField(
        max_length=1,
        choices=[(str(x), str(x)) for x in range(1, 9)],
        default='1',
        verbose_name=_('Semester'))
    semester_type = models.CharField(
        max_length=1,
        choices=SEMESTER,
        default='1',
        verbose_name=_('Odd/Event'))
    sks_meeting = models.PositiveIntegerField(
        default=0, verbose_name=_("SKS Meeting"))
    sks_practice = models.PositiveIntegerField(
        default=0, verbose_name=_("SKS Practice"))
    sks_field_practice = models.PositiveIntegerField(
        default=0, verbose_name=_("SKS Field"))
    sks_simulation = models.PositiveIntegerField(
        default=0, verbose_name=_("SKS Simulation"))

    @property
    def sks_total(self):
        return self.sks_meeting + self.sks_practice + self.sks_field_practice + self.sks_simulation

    def __str__(self):
        return "{}".format(self.course)
