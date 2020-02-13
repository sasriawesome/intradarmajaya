from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import translation, timezone
from mptt.models import TreeForeignKey

from wagtail.search import index
from wagtail.documents.models import Document
from wagtail.core.models import Orderable
from modelcluster.models import ClusterableModel, ParentalKey

from wagtailkit.core.models import MAX_LEN_SHORT, MAX_LEN_MEDIUM, MAX_LEN_LONG, KitBaseModel
from wagtailkit.numerators.models import NumeratorMixin
from wagtailkit.organizations.models import Position
from wagtailkit.persons.models import Person, KKNILevel

_ = translation.gettext_lazy


class Employment(index.Indexed, KitBaseModel):
    class Meta:
        verbose_name = _('Employment')
        verbose_name_plural = _('Employments')

    name = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_('Name'))
    note = models.TextField(
        null=True, blank=True,
        max_length=MAX_LEN_LONG,
        verbose_name=_('Note'))

    search_fields = [
        index.SearchField('name', partial_match=True)
    ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Employment, self).save(*args, **kwargs)


class EmployeeManager(models.Manager):

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('person', 'position', 'employment', 'attachment')

    def get_summary(self):
        kontrak, created = Employment.objects.get_or_create(name='Kontrak', defaults={'name': 'Kontrak'})
        tetap, created = Employment.objects.get_or_create(name='Tetap', defaults={'name': 'Tetap'})
        outsource, created = Employment.objects.get_or_create(name='Outsource', defaults={'name': 'Outsource'})
        return self.get_queryset().aggregate(
            count_total=models.Count('id'),
            count_active=models.Count('id', filter=models.Q(is_active=True)),
            count_inactive=models.Count('id', filter=models.Q(is_active=False)),
            count_kontrak=models.Count('id', filter=models.Q(employment=kontrak)),
            count_tetap=models.Count('id', filter=models.Q(employment=tetap)),
            count_outsource=models.Count('id', filter=models.Q(employment=outsource)),
            count_sma_active=models.Count(
                'id', filter=models.Q(
                    person__last_education_level__in=[
                        KKNILevel.SD.value, KKNILevel.SMP.value, KKNILevel.SMA.value
                    ]) & models.Q(is_active=True)
            ),
            count_sma_inactive=models.Count(
                'id', filter=models.Q(
                    person__last_education_level__in=[
                        KKNILevel.SD.value, KKNILevel.SMP.value, KKNILevel.SMA.value
                    ]) & models.Q(is_active=False)
            ),
            count_d3_active=models.Count(
                'id', filter=models.Q(
                    person__last_education_level__in=[
                        KKNILevel.D3.value, KKNILevel.D2.value, KKNILevel.D1.value
                    ]) & models.Q(is_active=True)
            ),
            count_d3_inactive=models.Count(
                'id', filter=models.Q(
                    person__last_education_level__in=[
                        KKNILevel.D3.value, KKNILevel.D2.value, KKNILevel.D1.value
                    ]) & models.Q(is_active=False)
            ),
            count_s1_active=models.Count(
                'id', filter=models.Q(person__last_education_level=KKNILevel.S1.value) & models.Q(is_active=True)
            ),
            count_s1_inactive=models.Count(
                'id', filter=models.Q(person__last_education_level=KKNILevel.S1.value) & models.Q(is_active=False)
            ),
            count_s2_active=models.Count(
                'id', filter=models.Q(person__last_education_level=KKNILevel.S2.value) & models.Q(is_active=True)
            ),
            count_s2_inactive=models.Count(
                'id', filter=models.Q(person__last_education_level=KKNILevel.S2.value) & models.Q(is_active=False)
            ),
            count_s3_active=models.Count(
                'id', filter=models.Q(person__last_education_level=KKNILevel.S3.value) & models.Q(is_active=True)
            ),
            count_s3_inactive=models.Count(
                'id', filter=models.Q(person__last_education_level=KKNILevel.S3.value) & models.Q(is_active=False)
            ),
        )

    def get_by_natural_key(self, eid):
        return self.get(eid=eid)


class Employee(ClusterableModel, NumeratorMixin, KitBaseModel):
    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')

    doc_code = 'EMP'

    objects = EmployeeManager()

    eid = models.CharField(
        null=True, blank=False,
        max_length=MAX_LEN_SHORT,
        verbose_name=_('Employee ID'))
    person = models.OneToOneField(
        Person, on_delete=models.CASCADE,
        verbose_name=_("Person"))
    position = TreeForeignKey(
        Position,
        related_name='chairmans',
        on_delete=models.PROTECT,
        verbose_name=_('Position'))
    employment = models.ForeignKey(
        Employment, null=True, blank=True,
        on_delete=models.PROTECT,
        verbose_name=_("Employment"))
    date_registered = models.DateField(
        default=timezone.now, verbose_name=_('Date registered'))
    attachment = models.ForeignKey(
        Document, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name=_('Attachment'), help_text=_('Contract Document'))
    is_active = models.BooleanField(
        default=True, verbose_name=_("Active"))
    is_teacher_applicant = models.BooleanField(default=False, verbose_name=_('Teacher applicant'))

    def __str__(self):
        return str(self.person)

    def natural_key(self):
        natural_key = (self.eid,)
        return natural_key

    def force_teacher_status(self):
        teacher = getattr(self, 'teacher', None)
        if teacher:
            teacher.is_active = self.is_active

    def get_anchestors(self, ascending=True):
        return self.position.get_ancestors(ascending=ascending)

    def save(self, *args, **kwargs):
        self.force_teacher_status()
        super().save(*args, **kwargs)


class EmployeePersonalManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            models.Q(employee__isnull=False) | models.Q(is_employee_applicant=True)
        ).prefetch_related('employee')

    def get_by_natural_key(self, eid):
        return self.get(eid=eid)


class EmployeePersonal(Person):
    class Meta:
        verbose_name = _('Employee Personal')
        verbose_name_plural = _('Employee Personals')
        proxy = True

    objects = EmployeePersonalManager()

    @property
    def is_employee(self):
        return bool(getattr(self, 'employee', False))

    def save(self, *args, **kwargs):
        self.is_employee_applicant = True
        super().save(*args, **kwargs)


class ExtraPositionManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('position', 'employee')


class ExtraPosition(Orderable, KitBaseModel):
    class Meta:
        verbose_name = _('Chairman')
        verbose_name_plural = _('Chairmans')
        unique_together = ('employee', 'position')

    objects = ExtraPositionManager()

    position = TreeForeignKey(
        Position, on_delete=models.CASCADE,
        related_name='extra_chairmans',
        verbose_name=_("Position"))
    employee = ParentalKey(
        Employee, on_delete=models.CASCADE,
        related_name='extra_positions',
        verbose_name=_("Employee"))
    is_active = models.BooleanField(
        default=False, verbose_name=_("Active"))
    attachment = models.ForeignKey(
        Document, null=True, blank=True,
        on_delete=models.SET_NULL)

    def __str__(self):
        return "{}({})".format(self.employee, self.position)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
