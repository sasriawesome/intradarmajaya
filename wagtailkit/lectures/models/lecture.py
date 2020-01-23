from django.db import models
from django.utils import timezone, translation
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from wagtailkit.core.models import KitBaseModel, CreatorModelMixin, MAX_LEN_SHORT, MAX_LEN_LONG
from wagtailkit.numerators.models import NumeratorMixin
from wagtailkit.core.utils.datetime import add_time

from wagtailkit.academic.models import CurriculumCourse, SchoolYear
from wagtailkit.rooms.models import Room
from .faculty import Faculty
from .student import Student

_ = translation.gettext_lazy


class Lecture(CreatorModelMixin, KitBaseModel):
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
    name = models.CharField(
        max_length=MAX_LEN_SHORT,
        verbose_name=_('Name'))
    faculty = models.ForeignKey(
        Faculty, on_delete=models.CASCADE,
        related_name='lecture_faculty',
        verbose_name=_("Teacher"))
    assistant = models.ForeignKey(
        Faculty, on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='lecture_assistant',
        verbose_name=_("Assistant"))
    course = models.ForeignKey(
        CurriculumCourse, on_delete=models.CASCADE,
        verbose_name=_("Course"))
    school_year = models.ForeignKey(
        SchoolYear, on_delete=models.PROTECT,
        verbose_name=_("School year"))
    semester = models.CharField(
        max_length=4, choices=SEMESTER,
        default=ODD, verbose_name=_("Semester"))
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

    @property
    def default_time_end(self):
        return add_time(self.default_time_start, self.duration)

    def __str__(self):
        return ", ".join([self.code, str(self.faculty)])


class LectureScoreWeighting(CreatorModelMixin, KitBaseModel):
    class Meta:
        verbose_name = _("Lecture Score Weighting")
        verbose_name_plural = _("Lecture Score Weightings")

    lecture = models.OneToOneField(
        Lecture, on_delete=models.CASCADE,
        verbose_name=_("Lecture"))
    attendance = models.PositiveIntegerField(
        default=0, verbose_name=_("Attendance"))
    homework1 = models.PositiveIntegerField(
        default=0, verbose_name=_("Homework 1"))
    homework2 = models.PositiveIntegerField(
        default=0, verbose_name=_("Homework 2"))
    quis1 = models.PositiveIntegerField(
        default=0, verbose_name=_("Quis 1"))
    quis2 = models.PositiveIntegerField(
        default=0, verbose_name=_("Quis 2"))
    mid_exam = models.PositiveIntegerField(
        default=0, verbose_name=_("Mid Exam"))
    final_exam = models.PositiveIntegerField(
        default=0, verbose_name=_("Final Exam"))

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
        if self.total > 100:
            raise ValidationError(_(
                "Please correct all value, total weight greater than 100"
            ))

    def __str__(self):
        return str(self.lecture) + ' Score Weighting'


class LectureStudent(KitBaseModel):
    class Meta:
        verbose_name = _("Lecture Student")
        verbose_name_plural = _("Lecture Students")

    NEW = 'N'
    REPEAT = 'R'
    STATUS = (
        (NEW, _('New')),
        (REPEAT, _('Repeat'))
    )

    doc_code = 'LCT.ST'
    lecture = models.ForeignKey(
        Lecture, on_delete=models.CASCADE,
        verbose_name=_("Lecture"))
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE,
        verbose_name=_("Student"))
    status = models.CharField(
        max_length=3, choices=STATUS, default=NEW,
        verbose_name=_("Status"))

    def __str__(self):
        return ", ".join([str(self.student), str(self.lecture)])


class LectureScheduleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class LectureSchedule(NumeratorMixin, KitBaseModel):
    class Meta:
        verbose_name = _("Lecture Schedule")
        verbose_name_plural = _("Lecture Scehdules")

    MEETING = 'MEETING'
    ELEARNING = 'ELEARNING'
    SUBTITUTE = 'SUBTITUTE'
    MID_EXAM = 'MID_EXAM'
    FINAL_EXAM = 'FINAL_EXAM'
    STATUS = (
        (MEETING, _('Meeting')),
        (ELEARNING, _('E-Learning')),
        (SUBTITUTE, _('Subtitution')),
        (MID_EXAM, _('Mid Exam')),
        (FINAL_EXAM, _('Final Exam')),
    )

    doc_code = 'LCT.SC'

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
    room = models.ForeignKey(
        Room, on_delete=models.PROTECT,
        verbose_name=_("Room Name"))
    time_start = models.TimeField(
        default=timezone.now,
        verbose_name=_("Time start"))
    time_end = models.TimeField(
        default=timezone.now,
        verbose_name=_("Time end"))
    status = models.CharField(
        max_length=3, choices=STATUS, default=MEETING,
        verbose_name=_("Status"))

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

# TODO move to enrollment app
# class StudentEnrollment(NumeratorMixin, KitBaseModel):
#     class Meta:
#         verbose_name = _("Student Enrollment")
#         verbose_name_plural = _("Student Enrollments")
#
#     doc_code = 'KRS'
#     student = models.ForeignKey(
#         Student, on_delete=models.CASCADE,
#         verbose_name=_("Student"))
#     courses = models.ManyToManyField(
#         CurriculumCourse, verbose_name=_('Course')
#     )

class StudentScore(KitBaseModel):
    class Meta:
        verbose_name = _("Student Score")
        verbose_name_plural = _("Student Scores")
        unique_together = ('lecture', 'student')

    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.CASCADE,
        verbose_name=_("Lecture"))
    student = models.ForeignKey(
        LectureStudent, on_delete=models.CASCADE,
        verbose_name=_("Lecture student"))
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

    def __str__(self):
        return str(self.student) + ' Scores'



class LectureStudentAttendant(KitBaseModel):
    class Meta:
        verbose_name = _("Lecture Student Attendant")
        verbose_name_plural = _("Lecture Student Attendants")
        unique_together = ('schedule', 'student')

    PRESENT = 'PR'
    SICK = 'SC'
    ABSENT = 'AB'
    PERMIT = 'PR'
    STATUS = (
        (PRESENT, _('Present')),
        (SICK, _('Sick')),
        (ABSENT, _('Absent')),
        (PERMIT, _('Permit')),
    )

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE,
        verbose_name=_("Student"))
    schedule = models.ForeignKey(
        LectureSchedule, on_delete=models.CASCADE,
        verbose_name=_("Schedule"))
    status = models.CharField(
        max_length=3, choices=STATUS,
        default=PRESENT, verbose_name=_("Status"))
    note = models.CharField(
        max_length=MAX_LEN_LONG,
        null=True, blank=True,
        verbose_name=_("Note"))


class LectureTeacherAttendant(KitBaseModel):
    class Meta:
        verbose_name = _("Lecture Teacher Attendant")
        verbose_name_plural = _("Lecture Teacher Attendants")
        unique_together = ('schedule', 'faculty')

    PRESENT = 'PR'
    SICK = 'SC'
    ABSENT = 'AB'
    PERMIT = 'PR'
    STATUS = (
        (PRESENT, _('Present')),
        (SICK, _('Sict')),
        (ABSENT, _('Absent')),
        (PERMIT, _('Permit')),
    )

    schedule = models.ForeignKey(
        LectureSchedule, on_delete=models.CASCADE,
        verbose_name=_("Schedule"))
    faculty = models.ForeignKey(
        Faculty, on_delete=models.CASCADE,
        verbose_name=_("Teacher"))
    status = models.CharField(
        max_length=3, choices=STATUS,
        default=PRESENT, verbose_name=_("Status")),
    note = models.CharField(
        max_length=MAX_LEN_LONG,
        null=True, blank=True,
        verbose_name=_("Note"))
