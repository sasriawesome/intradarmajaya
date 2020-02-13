import enum
from datetime import datetime
from django.apps import apps
from django.db import models, transaction
from django.db.models.functions import Coalesce, Concat
from django.utils import timezone, translation, text

from mptt.models import MPTTModel, TreeForeignKey, TreeManager

from wagtail.search import index
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Orderable
from modelcluster.models import ClusterableModel, ParentalKey

from wagtailkit.core.models import (
    MAX_LEN_MEDIUM, MAX_LEN_LONG, MAX_RICHTEXT,
    KitBaseModel, CreatorModelMixin)
from wagtailkit.numerators.models import NumeratorMixin, Numerator
from wagtailkit.persons.models import KKNILevel
_ = translation.gettext_lazy



class RMULevel(enum.Enum):
    UNIVERSITY = '1'
    FACULTY = '2'
    MAJOR = '3'
    PROGRAM_STUDY = '4'

class Semester(enum.Enum):
    ODD = '1'
    EVEN = '2'
    SHORT = '3'


def count_subquery(model, extra_filter=None):
    filter = {'rmu_id': models.OuterRef('pk')}
    if extra_filter:
        filter.update(extra_filter)
    sqs = Coalesce(
        models.Subquery(
            model.objects.filter(**filter).order_by().values('rmu_id').annotate(
                total=models.Count('*')
            ).values('total'),
            output_field=models.IntegerField()
        ), 0)
    return sqs


def cumulative_count_subquery(model, extra_filter=None):
    filter = {
        'rmu__tree_id': models.OuterRef('tree_id'),
        'rmu__lft__gte': models.OuterRef('lft'),
        'rmu__lft__lte': models.OuterRef('rght')
    }
    if extra_filter:
        filter.update(extra_filter)
    sqs = Coalesce(
        models.Subquery(
            model.objects.filter(
                **filter
            ).order_by().values('rmu__tree_id').annotate(
                total=models.Count('*')
            ).values('total'),
            output_field=models.IntegerField()
        ), 0)
    return sqs


class ResourceManagementUnitManager(TreeManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).select_related('parent')

    def get_summary(self, *args, **kwargs):
        Course = apps.get_model('academic', model_name='Course', require_ready=True)
        Teacher = apps.get_model('teachers', model_name='Teacher', require_ready=True)
        Student = apps.get_model('students', model_name='Student', require_ready=True)

        return self.get_queryset(*args, **kwargs).annotate(
            total_courses=count_subquery(Course, {'is_active': True}),
            total_cum_courses=cumulative_count_subquery(Course, {'is_active': True}),
            total_teachers=count_subquery(Teacher, {'is_active': True}),
            total_cum_teachers=cumulative_count_subquery(Teacher, {'is_active': True}),
            total_students=count_subquery(Student, {'status': 'ACT'}),
            total_cum_students=cumulative_count_subquery(Student, {'status': 'ACT'}),
        )

    def get_with_summary(self, rmu_queryset=None):
        Course = apps.get_model('academic', model_name='Course', require_ready=True)
        Teacher = apps.get_model('teachers', model_name='Teacher', require_ready=True)
        Student = apps.get_model('students', model_name='Student', require_ready=True)

        if not rmu_queryset:
            rmu_queryset = self.get_queryset()

        return rmu_queryset.annotate(
            total_courses=count_subquery(Course),
            total_cum_courses=cumulative_count_subquery(Course),
            total_teachers=count_subquery(Teacher),
            total_cum_teachers=cumulative_count_subquery(Teacher),
            total_students=count_subquery(Student),
            total_cum_students=cumulative_count_subquery(Student),
        )


class ResourceManagementUnit(index.Indexed, CreatorModelMixin, MPTTModel, KitBaseModel):
    class Meta:
        verbose_name = _("Resource Management Unit")
        verbose_name_plural = _("Resource Management Unit")

    UNIVERSITY = '1'
    FACULTY = '2'
    MAJOR = '3'
    PROGRAM_STUDY = '4'

    LEVEL = (
        (UNIVERSITY, _('University')),
        (FACULTY, _('Faculty')),
        (MAJOR, _('Major')),
        (PROGRAM_STUDY, _('Program Study')),
    )

    objects = ResourceManagementUnitManager()

    parent = TreeForeignKey(
        'academic.ResourceManagementUnit',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Parent'))
    code = models.SlugField(
        unique=True,
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Code"))
    number = models.CharField(
        max_length=2,
        verbose_name=_("Number"))
    name = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Name"))
    status = models.CharField(
        max_length=3,
        choices=LEVEL,
        default=PROGRAM_STUDY,
        verbose_name=_('Status'))

    search_fields = [
        index.SearchField('name', partial_match=True),
        index.SearchField('code', partial_match=True),
    ]

    # Wagtail Autocomplete
    autocomplete_search_field = 'name'

    def autocomplete_label(self):
        # Wagtail Autocomplete Label
        return "{}".format(self.name)

    def __str__(self):
        return self.name


class ProgramStudyManager(ResourceManagementUnitManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(status=ResourceManagementUnit.PROGRAM_STUDY)


class ProgramStudy(ResourceManagementUnit):
    class Meta:
        verbose_name = _("Program Study")
        verbose_name_plural = _("Program Studies")
        proxy = True

    objects = ProgramStudyManager()

    # Wagtail Autocomplete
    autocomplete_search_field = 'name'

    def autocomplete_label(self):
        # Wagtail Autocomplete Label
        return "{}".format(self.name)


class SchoolYear(ClusterableModel, KitBaseModel):
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

    # Wagtail Autocomplete
    autocomplete_search_field = 'code'

    def autocomplete_label(self):
        # Wagtail Autocomplete Label
        return "{}".format(self.code)

    def create_code(self):
        return "{}/{}".format(self.year_start, self.year_end)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        self.code = self.create_code()
        super().save(*args, **kwargs)


class AcademicYear(ClusterableModel, KitBaseModel):
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
    date_start = models.DateField(
        verbose_name=_("Date start"))
    date_end = models.DateField(
        verbose_name=_("Date end"))

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        self.code = "{} S{}".format(self.school_year, self.semester)
        super().save(*args, **kwargs)


class AcademicActivity(Orderable, KitBaseModel):
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

    school_year = ParentalKey(
        SchoolYear, on_delete=models.PROTECT,
        related_name='academic_activities',
        verbose_name=_('Academic Year'))
    academic_year = ParentalKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name='semester_activities',
        verbose_name=_('Semester Year'))
    date_start = models.DateField(
        verbose_name=_("Date start"))
    date_end = models.DateField(
        verbose_name=_("Date end"))
    activity = RichTextField(
        verbose_name=_("Activity"))
    rmu = TreeForeignKey(
        ResourceManagementUnit,
        on_delete=models.PROTECT,
        verbose_name=_("RMU"),
        help_text=_("Resource Management Unit"))

    @property
    def status(self):
        list_date_start = (
            self.date_start.year,
            self.date_start.month,
            self.date_start.day
        )
        list_date_end = (
            self.date_end.year,
            self.date_end.month,
            self.date_end.day
        )
        activity_date_start = timezone.make_aware(
            timezone.datetime(*list_date_start))
        activity_date_end = timezone.make_aware(
            timezone.datetime(*list_date_end, hour=23, minute=59, second=59))

        cond1 = activity_date_start > timezone.make_aware(datetime.now())
        cond2 = activity_date_start <= timezone.make_aware(datetime.now()) <= activity_date_end
        cond3 = timezone.make_aware(datetime.now()) > activity_date_end

        if cond1:
            return AcademicActivity.STATUS[0][1]
        if cond2:
            return AcademicActivity.STATUS[1][1]
        if cond3:
            return AcademicActivity.STATUS[2][1]
        else:
            return 'Not Defined'

    def __str__(self):
        return "{} ({}/{})".format(
            self.academic_year,
            self.date_start.strftime('%d%m%Y'),
            self.date_end.strftime('%d%m%Y'),
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class CourseType(KitBaseModel):
    class Meta:
        verbose_name = _("Course Type")
        verbose_name_plural = _("Course Types")
        ordering = ('code',)

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
        return "{}".format(self.name)


class CourseGroup(KitBaseModel):
    class Meta:
        verbose_name = _("Course Group")
        verbose_name_plural = _("Course Groups")
        ordering = ('code',)

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
        return "{}".format(self.name)


class CourseManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).select_related(
            'rmu', 'course_type', 'course_group'
        )


class Course(index.Indexed, ClusterableModel, NumeratorMixin, KitBaseModel):
    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")
        ordering = ('inner_id',)

    numbering = Numerator.FIXED

    rmu = TreeForeignKey(
        ResourceManagementUnit,
        on_delete=models.PROTECT,
        related_name='courses',
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
    level = models.CharField(
        max_length=3,
        choices=[(str(lvl.value), str(lvl.name)) for lvl in KKNILevel],
        default=KKNILevel.S1,
        verbose_name=_('Level'))
    year_offered = models.CharField(
        max_length=3,
        choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')],
        default='1',
        verbose_name=_('Year Offered'))
    description = RichTextField(
        null=True, blank=True,
        max_length=MAX_RICHTEXT,
        verbose_name=_("Description"))
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

    search_fields = [
        index.SearchField('name', partial_match=True),
        index.SearchField('inner_id', partial_match=True),
        index.FilterField('rmu'),
    ]

    def __str__(self):
        return "{}, {}".format(self.inner_id, self.name)

    def get_requisite(self):
        prerequesite = getattr(self, 'course_courseprerequisite', None)
        return [] if not prerequesite else prerequesite.all()

    @property
    def has_syllabus(self):
        return bool(getattr(self, 'syllabuses').count())

    @property
    def prerequisite(self):
        req = ", ".join([str(i.requisite.name) for i in self.get_requisite()])
        return req

    def generate_inner_id(self):
        form = [
            self.rmu.code,
            self.course_type.code,
            self.course_group.code,
            self.level,
            self.year_offered,
            str(self.reg_number).zfill(2)
        ]
        self.inner_id = '{}{}{}{}{}{}'.format(*form)
        return self.inner_id

    def get_counter(self):
        custom_code = self.get_custom_code()
        ct_counter = Numerator.get_instance(self, custom_code=custom_code)
        return ct_counter

    def get_custom_code(self):
        form = [self.rmu.code, self.course_type.code, self.course_group.code]
        return '{}{}{}'.format(*form)

    def get_teachers(self):
        teachers = getattr(self, 'teacher_set', None)
        return [] if not teachers else teachers.all()

    def save(self, **kwargs):
        super().save(**kwargs)


class CoursePreRequisite(Orderable, KitBaseModel):
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
    course = ParentalKey(
        Course,
        related_name="course_prerequisites",
        on_delete=models.CASCADE,
        verbose_name=_("Course"))
    requisite = models.ForeignKey(
        Course, null=True, blank=True,
        related_name="prerequisites",
        on_delete=models.CASCADE, verbose_name=_("Requisite"))
    score = models.CharField(
        max_length=2, default='C',
        choices=SCORE,
        verbose_name=_('Min Graduated Score'))

    def __str__(self):
        return ", ".join([str(self.course.name), str(self.requisite.name)])


class CurriculumManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('curriculum_courses').select_related('rmu')

    def get_with_summary(self, curriculum_queryset=None):
        """
            Course type:
            m = mandaroty, c = choice, i = interest, r = research
            Course rmu:
            u = university, f = faculty, m = major, p = program study
        """
        # make sure queryset is available
        if not curriculum_queryset:
            curriculum_queryset = self.get_queryset()

        filter_sks_mu = (
            models.Q(curriculum_courses__course__course_type__code='1')
            & models.Q(curriculum_courses__course__rmu__status='1'))
        filter_sks_cu = (
            models.Q(curriculum_courses__course__course_type__code='2')
            & models.Q(curriculum_courses__course__rmu__status='1'))
        filter_sks_iu = (
            models.Q(curriculum_courses__course__course_type__code='3')
            & models.Q(curriculum_courses__course__rmu__status='1'))
        filter_sks_ru = (
            models.Q(curriculum_courses__course__course_type__code='4')
            & models.Q(curriculum_courses__course__rmu__status='1'))

        # faculty courses
        filter_sks_mf = (
            models.Q(curriculum_courses__course__course_type__code='1')
            & models.Q(curriculum_courses__course__rmu__status='2'))
        filter_sks_cf = (
            models.Q(curriculum_courses__course__course_type__code='2')
            & models.Q(curriculum_courses__course__rmu__status='2'))
        filter_sks_if = (
            models.Q(curriculum_courses__course__course_type__code='3')
            & models.Q(curriculum_courses__course__rmu__status='2'))
        filter_sks_rf = (
            models.Q(curriculum_courses__course__course_type__code='4')
            & models.Q(curriculum_courses__course__rmu__status='2'))

        # major courses
        filter_sks_mm = (
            models.Q(curriculum_courses__course__course_type__code='1')
            & models.Q(curriculum_courses__course__rmu__status='3'))
        filter_sks_cm = (
            models.Q(curriculum_courses__course__course_type__code='2')
            & models.Q(curriculum_courses__course__rmu__status='3'))
        filter_sks_im = (
            models.Q(curriculum_courses__course__course_type__code='3')
            & models.Q(curriculum_courses__course__rmu__status='3'))
        filter_sks_rm = (
            models.Q(curriculum_courses__course__course_type__code='4')
            & models.Q(curriculum_courses__course__rmu__status='3'))

        # program courses
        filter_sks_mp = (
            models.Q(curriculum_courses__course__course_type__code='1')
            & models.Q(curriculum_courses__course__rmu__status='4'))
        filter_sks_cp = (
            models.Q(curriculum_courses__course__course_type__code='2')
            & models.Q(curriculum_courses__course__rmu__status='4'))
        filter_sks_ip = (
            models.Q(curriculum_courses__course__course_type__code='3')
            & models.Q(curriculum_courses__course__rmu__status='4'))
        filter_sks_rp = (
            models.Q(curriculum_courses__course__course_type__code='4')
            & models.Q(curriculum_courses__course__rmu__status='4'))

        return curriculum_queryset.select_related('rmu').prefetch_related(
            'curriculum_courses'
        ).annotate(
            # university courses
            sks_mu=Coalesce(models.Sum('curriculum_courses__sks_total', filter=filter_sks_mu), 0),
            sks_cu=Coalesce(models.Sum('curriculum_courses__sks_total', filter=filter_sks_cu), 0),
            sks_iu=Coalesce(models.Sum('curriculum_courses__sks_total', filter=filter_sks_iu), 0),
            sks_ru=Coalesce(models.Sum('curriculum_courses__sks_total', filter=filter_sks_ru), 0),
            sks_tu=models.F('sks_mu') + models.F('sks_cu') + models.F('sks_iu') + models.F('sks_ru'),

            # faculty courses
            sks_mf=Coalesce(models.Sum('curriculum_courses__sks_total', filter=filter_sks_mf), 0),
            sks_cf=Coalesce(models.Sum('curriculum_courses__sks_total', filter=filter_sks_cf), 0),
            sks_if=Coalesce(models.Sum('curriculum_courses__sks_total', filter=filter_sks_if), 0),
            sks_rf=Coalesce(models.Sum('curriculum_courses__sks_total', filter=filter_sks_rf), 0),
            sks_tf=models.F('sks_mf') + models.F('sks_cf') + models.F('sks_if') + models.F('sks_rf'),

            # major courses
            sks_mm=Coalesce(models.Sum('curriculum_courses__sks_total', filter=filter_sks_mm), 0),
            sks_cm=Coalesce(models.Sum('curriculum_courses__sks_total', filter=filter_sks_cm), 0),
            sks_im=Coalesce(models.Sum('curriculum_courses__sks_total', filter=filter_sks_im), 0),
            sks_rm=Coalesce(models.Sum('curriculum_courses__sks_total', filter=filter_sks_rm), 0),
            sks_tm=models.F('sks_mm') + models.F('sks_cm') + models.F('sks_im') + models.F('sks_rm'),

            # program courses
            sks_mp=Coalesce(models.Sum('curriculum_courses__sks_total', filter=filter_sks_mp), 0),
            sks_cp=Coalesce(models.Sum('curriculum_courses__sks_total', filter=filter_sks_cp), 0),
            sks_ip=Coalesce(models.Sum('curriculum_courses__sks_total', filter=filter_sks_ip), 0),
            sks_rp=Coalesce(models.Sum('curriculum_courses__sks_total', filter=filter_sks_rp), 0),
            sks_tp=models.F('sks_mp') + models.F('sks_cp') + models.F('sks_ip') + models.F('sks_rp'),

            sks_mandatory=models.F('sks_mu') + models.F('sks_mf') + models.F('sks_mm') + models.F('sks_mp'),
            sks_choice=models.F('sks_cu') + models.F('sks_cf') + models.F('sks_cm') + models.F('sks_cp'),
            sks_interest=models.F('sks_iu') + models.F('sks_if') + models.F('sks_im') + models.F('sks_ip'),
            sks_research=models.F('sks_ru') + models.F('sks_rf') + models.F('sks_rm') + models.F('sks_rp'),

            sks_meeting=Coalesce(models.Sum('curriculum_courses__sks_meeting'), 0),
            sks_practice=Coalesce(models.Sum('curriculum_courses__sks_practice'), 0),
            sks_field_practice=Coalesce(models.Sum('curriculum_courses__sks_field_practice'), 0),
            sks_simulation=Coalesce(models.Sum('curriculum_courses__sks_simulation'), 0),
            sks_total=models.F('sks_meeting')
                      + models.F('sks_practice')
                      + models.F('sks_field_practice')
                      + models.F('sks_simulation')
        )


class Curriculum(ClusterableModel, KitBaseModel):
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
    rmu = TreeForeignKey(
        ProgramStudy,
        on_delete=models.PROTECT,
        verbose_name=_("Program Study"),
        help_text=_("Resource Management Unit"))
    name = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Name"))
    sks_graduate = models.PositiveIntegerField(
        default=0,
        verbose_name=_("SKS graduate"))
    is_active = models.BooleanField(
        default=True, verbose_name=_('Active'))

    def __str__(self):
        return self.name

    def create_code(self):
        self.code = "".join([self.rmu.code, self.year])

    def create_name(self):
        self.name = "{} {}".format(self.rmu.name, self.year)

    def save(self, *args, **kwargs):
        # Todo Next
        # self.create_code()
        # self.create_name()
        super(Curriculum, self).save(*args, **kwargs)

    def get_summary(self):
        return Curriculum.objects.get_with_summary().get(pk=self.id)

    def get_courses_by_semester(self):
        """
        semester_list = [
            {
                semester: 1,
                total_course: 3,
                total_sks: 24
                semester_courses: [CourseObject1 ... CourseObjectn],
            }
        ]
        """
        curriculum_courses = getattr(self, 'curriculum_courses', None)
        semester = []
        semester_list = []
        for course in curriculum_courses.all():
            if course.semester_number not in semester:
                semester.append(course.semester_number)
        for sms in semester:
            current_courses = curriculum_courses.filter(semester_number=sms)
            semester_list.append({
                'semester': sms,
                'course_count': len(current_courses.values('id')),
                'sks_meeting': sum(map(lambda x: x.sks_meeting, current_courses)),
                'sks_practice': sum(map(lambda x: x.sks_practice, current_courses)),
                'sks_field_practice': sum(map(lambda x: x.sks_field_practice, current_courses)),
                'sks_simulation': sum(map(lambda x: x.sks_simulation, current_courses)),
                'sks_total': sum(map(lambda x: x.sks_total, current_courses)),
                'semester_courses': current_courses.all()
            })
        return semester_list


class CurricullumCourseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'curriculum', 'course'
        ).annotate(
            course_inner_id=models.F('course__inner_id'),
            course_name=models.F('course__name'),
        )


class CurriculumCourse(Orderable, KitBaseModel):
    class Meta:
        verbose_name = _("Curricullum Course")
        verbose_name_plural = _("Curricullum Courses")
        unique_together = ('curriculum', 'course')
        ordering = ('curriculum', 'semester_number',)

    SEMESTER = (
        ('1', _('Odd')),
        ('2', _('Even')),
    )

    objects = CurricullumCourseManager()

    curriculum = ParentalKey(
        Curriculum, on_delete=models.CASCADE,
        related_name='curriculum_courses',
        verbose_name=_("Curriculum"))
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE,
        related_name='course_curriculums',
        verbose_name=_("Course"))
    semester_number = models.CharField(
        max_length=1, default='1',
        choices=[(str(x), str(x)) for x in range(1, 9)],
        verbose_name=_('Semester'))
    semester_type = models.CharField(
        max_length=1, choices=SEMESTER, default='1',
        verbose_name=_('Odd/Event'))
    sks_meeting = models.PositiveIntegerField(
        default=0, verbose_name=_("SKS Meeting"))
    sks_practice = models.PositiveIntegerField(
        default=0, verbose_name=_("SKS Practice"))
    sks_field_practice = models.PositiveIntegerField(
        default=0, verbose_name=_("SKS Field"))
    sks_simulation = models.PositiveIntegerField(
        default=0, verbose_name=_("SKS Simulation"))
    sks_total = models.PositiveIntegerField(
        editable=False, default=0,
        verbose_name=_("SKS Total"))

    def __str__(self):
        return self.course.name

    def save(self, *args, **kwargs):
        self.sks_total = (
            self.sks_meeting
            + self.sks_practice
            + self.sks_field_practice
            + self.sks_simulation
        )
        super().save(*args, **kwargs)


class CourseEqualizer(ClusterableModel, KitBaseModel):
    class Meta:
        verbose_name = _("Course Equalizer")
        verbose_name_plural = _("Course Equalizers")
        unique_together = ('old_course', 'new_course')

    old_course = models.ForeignKey(
        CurriculumCourse,
        on_delete=models.PROTECT,
        related_name='old_courses',
        verbose_name=_('Old Course'))
    sks_old_course = models.IntegerField(
        verbose_name=_('SKS Old'))
    new_course = models.ForeignKey(
        CurriculumCourse,
        on_delete=models.PROTECT,
        related_name='new_courses',
        verbose_name=_('New Course'))
    sks_new_course = models.IntegerField(
        verbose_name=_('SKS New'))

    def __str__(self):
        return "{}-{}".format(self.old_course, self.new_course)


class LearningMaterialBlock(blocks.StructBlock):
    class Meta:
        icon = 'cogs'
        group = True
        template = 'modeladmin/academic/syllabus/block/learning_material.html'

    name = blocks.CharBlock()
    description = blocks.CharBlock()
    type = blocks.ChoiceBlock(choices=[
        ('software', 'Software'),
        ('hardware', 'Hardware'),
        ('framework', 'Framework'),
        ('misc', 'Misc'),
    ], icon='cogs')


class ReferenceBlock(blocks.StructBlock):
    class Meta:
        icon = 'cogs'
        group = True
        template = 'modeladmin/academic/syllabus/block/reference.html'

    title = blocks.CharBlock()
    description = blocks.TextBlock()
    type = blocks.ChoiceBlock(choices=[
        ('book', 'Book'),
        ('journal', 'Journal'),
        ('article', 'Article'),
        ('sourcecode', 'Source Code'),
        ('documentation', 'Documentation'),
        ('misc', 'Misc'),
    ], icon='cogs')


class Syllabus(ClusterableModel, NumeratorMixin, CreatorModelMixin, KitBaseModel):
    class Meta:
        verbose_name = _("Syllabus")
        verbose_name_plural = _("Syllabuses")

    title = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_('Name'))
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE,
        related_name='syllabuses',
        verbose_name=_('Course'))
    description = RichTextField(
        max_length=MAX_RICHTEXT,
        verbose_name=_('Description'))
    body = StreamField([
        ('topic', blocks.RichTextBlock(label="Topic", group=True)),
        ('competency', blocks.RichTextBlock(label="Competency", group=True)),
        ('learning_material', LearningMaterialBlock()),
        ('reference', ReferenceBlock())
    ])

    def generate_inner_id(self):
        form = [
            self.course.inner_id,
            str(self.reg_number).zfill(2)]
        self.inner_id = 'SIL.{}.{}'.format(*form)
        return self.inner_id

    def get_counter(self):
        custom_code = self.get_custom_code()
        ct_counter = Numerator.get_instance(self, custom_code=custom_code)
        return ct_counter

    def get_custom_code(self):
        form = [self.course.inner_id]
        return 'SIL.{}'.format(*form)

    def __str__(self):
        return self.title


class ProgramUnit(blocks.StructBlock):
    session = blocks.IntegerBlock()
    duration = blocks.IntegerBlock()
    topic = blocks.RichTextBlock()
    competency = blocks.RichTextBlock()


class LectureProgram(Orderable, NumeratorMixin, CreatorModelMixin, KitBaseModel):
    class Meta:
        verbose_name = _("Lecture Program")
        verbose_name_plural = _("Lecture Program")

    syllabus = ParentalKey(
        Syllabus, on_delete=models.CASCADE,
        related_name='lecture_programs',
        verbose_name=_('Syllabus'))
    programs = StreamField([
        ('program_unit', ProgramUnit())
    ])

    def generate_inner_id(self):
        form = [
            self.syllabus.inner_id,
            str(self.reg_number).zfill(2)]
        self.inner_id = 'SAP.{}.{}'.format(*form)
        return self.inner_id

    def get_counter(self):
        custom_code = self.get_custom_code()
        ct_counter = Numerator.get_instance(self, custom_code=custom_code)
        return ct_counter

    def get_custom_code(self):
        form = [self.syllabus.inner_id]
        return 'SAP.{}'.format(*form)

    def __str__(self):
        return self.inner_id
