from django.db import models
from django.utils import timezone, translation
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from wagtailkit.core.models import KitBaseModel, CreatorModelMixin, MAX_LEN_SHORT
from wagtailkit.core.utils.datetime import add_time

from wagtailkit.academic.models import CurriculumCourse, AcademicYear, ProgramStudy
from wagtailkit.rooms.models import Room
from wagtailkit.teachers.models import Teacher
from wagtailkit.students.models import Student
from wagtailkit.numerators.models import NumeratorMixin
from wagtailkit.evaluations.models import EvalQuestion, Evaluation

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
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE,
        related_name='lecture_teacher',
        verbose_name=_("Teacher"))
    assistant = models.ForeignKey(
        Teacher, on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='lecture_assistant',
        verbose_name=_("Assistant"))
    prodi = models.ForeignKey(
        ProgramStudy,
        on_delete=models.PROTECT,
        verbose_name=_("Program Study"))
    course = models.ForeignKey(
        CurriculumCourse, on_delete=models.CASCADE,
        verbose_name=_("Course"))
    semester = models.ForeignKey(
        AcademicYear, on_delete=models.PROTECT,
        verbose_name=_("Academic year"))
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


class LectureStudent(KitBaseModel):
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
        Student, on_delete=models.CASCADE,
        verbose_name=_("Student"))
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


class LectureEvaluation(NumeratorMixin, CreatorModelMixin, KitBaseModel):
    class Meta:
        verbose_name = _("Lecture Evaluation")
        verbose_name_plural = _("Lecture Evaluations")

    doc_code = 'LEV'

    lecture = models.ForeignKey(
        Lecture, on_delete=models.CASCADE,
        verbose_name=_("Lecture"))
    student = models.ForeignKey(
        Student, null=True, blank=False,
        on_delete=models.SET_NULL,
        verbose_name=_("Student"))
    evaluation = models.ForeignKey(
        Evaluation, on_delete=models.PROTECT,
        verbose_name=_('Evaluation'))

    @property
    def title(self):
        return "Evaluasi {} oleh {}".format(self.lecture, self.student)

    def __str__(self):
        return self.title


class LectureEvaluationScore(KitBaseModel):
    class Meta:
        verbose_name = _("Lecture Evaluation Score")
        verbose_name_plural = _("Lecture Evaluation Scores")
        ordering = ('question__group__code', 'question__date_created',)

    lecture_evaluation = models.ForeignKey(
        LectureEvaluation, on_delete=models.CASCADE,
        verbose_name=_("Lecture evaluation"))
    question = models.ForeignKey(
        EvalQuestion, on_delete=models.PROTECT,
        verbose_name=_("Question"))
    score = models.PositiveIntegerField(
        choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'),),
        help_text=_('1:Tidak Setuju > 5:Setuju'),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        default=3, verbose_name=_('Score'))

    @staticmethod
    @receiver(post_save, sender=LectureEvaluation)
    def create_evaluation_questions(sender, **kwargs):
        created = kwargs.pop('created', False)
        instance = kwargs.pop('instance', None)
        if created:
            questions = []
            for question in instance.evaluation.questions.all():
                lect_question = LectureEvaluationScore(
                    lecture_evaluation=instance,
                    question=question)
                questions.append(lect_question)
            LectureEvaluationScore.objects.bulk_create(questions)

    def __str__(self):
        return self.question.group.name
