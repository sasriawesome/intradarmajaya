from django.db import models
from django.utils import timezone, translation
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from wagtailkit.core.models import KitBaseModel, CreatorModelMixin, MAX_LEN_SHORT
from wagtailkit.core.utils.datetime import add_time
from wagtail.core.models import Orderable
from modelcluster.models import ClusterableModel, ParentalKey

from wagtailkit.academic.models import CurriculumCourse, AcademicYear, ResourceManagementUnit
from wagtailkit.rooms.models import Room
from wagtailkit.teachers.models import Teacher
from wagtailkit.students.models import Student, StudentScore

_ = translation.gettext_lazy


class Lecture(ClusterableModel, CreatorModelMixin, KitBaseModel):
    class Meta:
        verbose_name = _("Lecture")
        verbose_name_plural = _("Lectures")

    PENDING = 'PND'
    ONGOING = 'ONG'
    END = 'END'
    STATUS = (
        (PENDING, _('Pending')),
        (ONGOING, _('On Going')),
        (END, _('End')),
    )

    doc_code = 'LCT'
    ODD = 'odd'
    EVEN = 'even'
    SHORT = 'short'
    SEMESTER = (
        (ODD, _('Odd')),
        (EVEN, _('Even')),
        (SHORT, _('Short'))
    )

    code = models.CharField(
        max_length=MAX_LEN_SHORT,
        verbose_name=_('Code'))
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE,
        related_name='lecture_teacher',
        verbose_name=_("Teacher"))
    assistant = models.ForeignKey(
        Teacher, on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='lecture_assistant',
        verbose_name=_("Assistant"))
    rmu = models.ForeignKey(
        ResourceManagementUnit,
        on_delete=models.PROTECT,
        verbose_name=_("Program Study"))
    course = models.ForeignKey(
        CurriculumCourse,
        on_delete=models.CASCADE,
        verbose_name=_("Course"))
    academic_year = models.ForeignKey(
        AcademicYear, on_delete=models.PROTECT,
        verbose_name=_("Academic Year"))
    room = models.ForeignKey(
        Room, on_delete=models.PROTECT,
        verbose_name=_("Room Name"))
    date_start = models.DateField(
        default=timezone.now, verbose_name="Date start")
    default_time_start = models.TimeField(
        default=timezone.now, verbose_name=_("Time start"))
    duration = models.PositiveIntegerField(
        verbose_name=_('Duration'),
        help_text=_("Lecture duration in minutes"))
    series = models.PositiveIntegerField(
        verbose_name=_('Series'),
        help_text=_("Total Meet Up"))
    status = models.CharField(
        max_length=3, choices=STATUS, default=PENDING,
        verbose_name=_("Status"))

    autocomplete_search_field = 'code'

    def autocomplete_label(self):
        return "{} | {} | {}".format(self.code, self.course, self.teacher)

    @property
    def default_time_end(self):
        return add_time(self.default_time_start, self.duration)

    def __str__(self):
        return "{} - {} ({})".format(self.code, str(self.course), str(self.teacher))


class LectureScoreWeighting(CreatorModelMixin, KitBaseModel):
    class Meta:
        verbose_name = _("Lecture Score Weighting")
        verbose_name_plural = _("Lecture Score Weightings")

    lecture = models.OneToOneField(
        Lecture, on_delete=models.CASCADE,
        verbose_name=_("Lecture"))
    attendance = models.PositiveIntegerField(
        default=15, verbose_name=_("Attendance"))
    homework1 = models.PositiveIntegerField(
        default=10, verbose_name=_("Homework 1"))
    homework2 = models.PositiveIntegerField(
        default=10, verbose_name=_("Homework 2"))
    quis1 = models.PositiveIntegerField(
        default=10, verbose_name=_("Quis 1"))
    quis2 = models.PositiveIntegerField(
        default=10, verbose_name=_("Quis 2"))
    mid_exam = models.PositiveIntegerField(
        default=20, verbose_name=_("Mid Exam"))
    final_exam = models.PositiveIntegerField(
        default=25, verbose_name=_("Final Exam"))

    @property
    def total(self):
        total = (self.attendance
                 + self.homework1
                 + self.homework2
                 + self.quis1
                 + self.quis2
                 + self.mid_exam
                 + self.final_exam)
        return total

    def clean(self):
        if self.total != 100:
            raise ValidationError(_(
                "Please correct all value, total weight must be 100% current total is {}"
            ).format(self.total))

    def __str__(self):
        return str(self.lecture) + ' Score Weighting'


class LectureStudentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('student', 'lecture')


class LectureStudent(Orderable, KitBaseModel):
    class Meta:
        verbose_name = _("Lecture Student")
        verbose_name_plural = _("Lecture Students")
        unique_together = ('lecture', 'student')

    NEW = 'N'
    REPEAT = 'R'
    STATUS = (
        (NEW, _('New')),
        (REPEAT, _('Repeat'))
    )

    objects = LectureStudentManager()

    lecture = ParentalKey(
        Lecture, on_delete=models.CASCADE,
        related_name='students',
        verbose_name=_("Lecture"))
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE,
        related_name='lectures',
        verbose_name=_("Student"))
    status = models.CharField(
        max_length=3, choices=STATUS, default=NEW,
        verbose_name=_("Status"))

    autocomplete_search_field = 'student__person__fullname'

    def autocomplete_label(self):
        return "{} - {} | {}".format(self.lecture.code, self.student.sid, self.student)

    def __str__(self):
        return ", ".join([str(self.student), str(self.lecture)])


class LectureScheduleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class LectureSchedule(KitBaseModel):
    class Meta:
        verbose_name = _("Lecture Schedule")
        verbose_name_plural = _("Lecture Schedules")

    MEETING = '1'
    ELEARNING = '2'
    MID_EXAM = '3'
    FINAL_EXAM = '4'
    SUBTITUTE = '99'
    TYPE = (
        (MEETING, _('Meeting')),
        (ELEARNING, _('E-Learning')),
        (SUBTITUTE, _('Subtitution')),
        (MID_EXAM, _('Mid Exam')),
        (FINAL_EXAM, _('Final Exam')),
    )

    lecture = models.ForeignKey(
        Lecture, on_delete=models.CASCADE,
        verbose_name=_("Lecture"))
    session = models.PositiveIntegerField(
        default=1, validators=[
            MinValueValidator(1),
            MaxValueValidator(50)],
        verbose_name=_('Session'))
    date = models.DateField(
        default=timezone.now,
        verbose_name="Date")
    time_start = models.TimeField(
        default=timezone.now,
        verbose_name=_("Time start"))
    time_end = models.TimeField(
        default=timezone.now,
        verbose_name=_("Time end"))
    room = models.ForeignKey(
        Room, on_delete=models.PROTECT,
        verbose_name=_("Room Name"))
    type = models.CharField(
        max_length=3, choices=TYPE, default=MEETING,
        verbose_name=_("Type"))

    autocomplete_search_field = 'lecture__course__course__name'

    def autocomplete_label(self):
        return "Session {} | {}".format(self.session, self.lecture)

    @property
    def status(self):
        list_date = (
            self.date.year, self.date.month, self.date.day)
        scedule_date_start = timezone.make_aware(
            timezone.datetime(
                *list_date,
                hour=self.time_start.hour,
                minute=self.time_start.minute,
                second=self.time_start.second))
        scedule_date_end = timezone.make_aware(
            timezone.datetime(
                *list_date,
                hour=self.time_end.hour,
                minute=self.time_end.minute,
                second=self.time_end.second))
        cond1 = timezone.now() >= scedule_date_start
        cond2 = timezone.now() <= scedule_date_end
        return True if cond1 and cond2 else False

    def __str__(self):
        return ", ".join(
            [str(self.lecture), str(self.session)])


class LectureScore(StudentScore):
    class Meta:
        verbose_name = _("Lecture Score")
        verbose_name_plural = _("Lecture Scores")

    lecture = models.ForeignKey(
        Lecture, null=True, blank=False,
        on_delete=models.SET_NULL,
        verbose_name=_("Lecture"))
    attendance = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        verbose_name=_("Attendance"))
    homework1 = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        verbose_name=_("Homework 1"))
    homework2 = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        verbose_name=_("Homework 2"))
    quis1 = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        verbose_name=_("Quis 1"))
    quis2 = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        verbose_name=_("Quis 2"))
    mid_exam = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        verbose_name=_("Mid Exam"))
    final_exam = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        verbose_name=_("Final Exam"))
    total_score = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        verbose_name=_("Total Score"))

    def save(self, **kwargs):
        self.course = self.lecture.course
        super().save(**kwargs)
