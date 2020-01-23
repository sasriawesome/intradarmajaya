import os
import uuid
from django.db import models, transaction
from django.core.validators import MinValueValidator, MaxValueValidator

from django.utils import translation, timezone
from wagtail.core.models import Orderable
from wagtail.documents.models import Document
from modelcluster.fields import ParentalKey

from wagtailkit.core.models import (
    MAX_LEN_MEDIUM, MAX_LEN_LONG,
    KitBaseModel
)

from .extra import EducationLevel
from .person import Person

_ = translation.gettext_lazy


def upload_attachment_to(instance, filename):
    filename, ext = os.path.splitext(filename)
    return os.path.join(
        'history_attachment',
        'history_attrachment_{uuid}_{filename}{ext}'.format(
            uuid=uuid.uuid4(), filename=filename, ext=ext)
    )


class FormalEducation(Orderable, KitBaseModel):
    class Meta:
        verbose_name = _('Formal Education')
        verbose_name_plural = _('Formal Educations')
        unique_together = ('person', 'level')

    FINISHED = 'FNS'
    ONGOING = 'ONG'
    UNFINISHED = 'UNF'
    STATUS = (
        (FINISHED, _("Finished")),
        (ONGOING, _("Ongoing")),
        (UNFINISHED, _("Unfinished"))
    )

    person = ParentalKey(
        Person, on_delete=models.CASCADE,
        related_name='education_histories',
        verbose_name=_("Person"))
    level = models.ForeignKey(
        EducationLevel,
        on_delete=models.PROTECT,
        verbose_name=_("Level"))
    institution_name = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Institution"))
    major = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        null=True, blank=True,
        verbose_name=_("Major"),
        help_text=_("ex: IPA, IPS, Information System or Accounting"))
    date_start = models.DateField(
        default=timezone.now,
        verbose_name=_("Date start"))
    date_end = models.DateField(
        default=timezone.now,
        verbose_name=_("Date end"))
    status = models.CharField(
        max_length=3, default=FINISHED, choices=STATUS,
        verbose_name=_("Current status"))
    attachment = models.ForeignKey(
        Document, null=True, blank=True,
        on_delete=models.SET_NULL)

    def __str__(self):
        return self.institution_name


class NonFormalEducation(Orderable, KitBaseModel):
    class Meta:
        verbose_name = _('Non Formal Education')
        verbose_name_plural = _('Non Formal Educations')

    FINISHED = 'FNS'
    ONGOING = 'ONG'
    UNFINISHED = 'UNF'
    STATUS = (
        (FINISHED, _("Finished")),
        (ONGOING, _("Ongoing")),
        (UNFINISHED, _("Unfinished"))
    )

    person = ParentalKey(
        Person, on_delete=models.CASCADE,
        related_name='nonformaleducation_histories',
        verbose_name=_("Person"))
    name = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Name"))
    institution_name = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Institution"))
    description = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        null=True, blank=True,
        verbose_name=_("Description"))
    date_start = models.DateField(
        default=timezone.now, verbose_name=_("Date start"))
    date_end = models.DateField(
        default=timezone.now, verbose_name=_("Date end"))
    status = models.CharField(
        max_length=3, default=FINISHED, choices=STATUS,
        verbose_name=_("Current status"))
    attachment = models.ForeignKey(
        Document, null=True, blank=True,
        on_delete=models.SET_NULL)

    def __str__(self):
        return self.institution_name


class Working(Orderable, KitBaseModel):
    class Meta:
        verbose_name = _('Working')
        verbose_name_plural = _('Workings')

    CONTRACT = 'CTR'
    FIXED = 'FXD'
    OUTSOURCE = 'OSR'
    STATUS = (
        (CONTRACT, _("Contract")),
        (FIXED, _("Fixed")),
        (OUTSOURCE, _("Outsource"))
    )

    person = ParentalKey(
        Person, on_delete=models.CASCADE,
        related_name='working_histories',
        verbose_name=_("Person"))
    institution_name = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Institution"))
    department = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Department"))
    position = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Position"))
    date_start = models.DateField(
        default=timezone.now, verbose_name=_("Date start"))
    date_end = models.DateField(
        default=timezone.now, verbose_name=_("Date end"))
    status = models.CharField(
        max_length=3, default=CONTRACT, choices=STATUS,
        verbose_name=_("Employment"))
    attachment = models.ForeignKey(
        Document, null=True, blank=True,
        on_delete=models.SET_NULL)

    def __str__(self):
        return "%s, %s" % (self.institution_name, self.position)


class Volunteer(Orderable, KitBaseModel):
    class Meta:
        verbose_name = _('Volunteer')
        verbose_name_plural = _('Volunteers')

    ACTIVE = 'ACT'
    INACTIVE = 'INC'
    STATUS = (
        (ACTIVE, _("Active")),
        (INACTIVE, _("Inactive")),
    )

    person = ParentalKey(
        Person, on_delete=models.CASCADE,
        related_name='organization_histories',
        verbose_name=_("Person"))
    organization = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Organization"))
    position = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Position"))
    description = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Description"))
    date_start = models.DateField(
        default=timezone.now, verbose_name=_("Date start"))
    date_end = models.DateField(
        default=timezone.now, verbose_name=_("Date end"))
    attachment = models.ForeignKey(
        Document, null=True, blank=True,
        on_delete=models.SET_NULL)
    status = models.CharField(
        max_length=3, default=ACTIVE, choices=STATUS,
        verbose_name=_("Status"))

    def __str__(self):
        return "%s, %s" % (self.organization, self.position)


class Award(Orderable, KitBaseModel):
    class Meta:
        verbose_name = _('Award')
        verbose_name_plural = _('Awards')

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4,
        editable=False, verbose_name=_('ID'))
    person = ParentalKey(
        Person, on_delete=models.CASCADE,
        related_name='awards',
        verbose_name=_("Person"))
    name = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Name"))
    description = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        null=True, blank=True,
        verbose_name=_("Description"))
    date = models.DateTimeField(
        null=True, blank=True,
        default=timezone.now,
        verbose_name=_('Created date'))
    attachment = models.ForeignKey(
        Document, null=True, blank=True,
        on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Skill(Orderable, KitBaseModel):
    class Meta:
        verbose_name = _('Skill')
        verbose_name_plural = _('Skills')

    person = ParentalKey(
        Person, on_delete=models.CASCADE,
        related_name='skill_sets',
        verbose_name=_("Person"))
    name = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Name"))
    description = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        null=True, blank=True,
        verbose_name=_("Description"))
    level = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name=_('Skill level'))

    def __str__(self):
        return self.name


class Family(Orderable, KitBaseModel):
    class Meta:
        verbose_name = _('Family')
        verbose_name_plural = _('Families')

    FATHER = '1'
    MOTHER = '2'
    SIBLING = '3'
    CHILD = '4'
    OTHER = '99'
    RELATION = (
        (FATHER, _('Father')),
        (MOTHER, _('Mother')),
        (SIBLING, _('Sibling')),
        (CHILD, _('Children')),
        (OTHER, _('Other')),
    )

    person = ParentalKey(
        Person, on_delete=models.CASCADE,
        related_name='families',
        verbose_name=_("Person"))
    relation = models.CharField(
        choices=RELATION, default=OTHER,
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("relation"))
    relationship = models.CharField(
        null=True, blank=True,
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Relationship"))
    name = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Name"))
    date_of_birth = models.DateField(
        null=True, blank=True,
        default=timezone.now,
        verbose_name=_('Date of birth'))
    place_of_birth = models.CharField(
        null=True, blank=True,
        max_length=255,
        verbose_name=_('Place of birth'))
    job = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Job"))
    address = models.TextField(
        max_length=MAX_LEN_LONG,
        null=True, blank=True,
        verbose_name=_("Address"))

    def __str__(self):
        return self.name


class Publication(Orderable, KitBaseModel):
    class Meta:
        verbose_name = _('Publication')
        verbose_name_plural = _('Publications')

    person = ParentalKey(
        Person, on_delete=models.CASCADE,
        related_name='publications',
        verbose_name=_("Person"))
    title = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Title"))
    description = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        null=True, blank=True,
        verbose_name=_("Description"))
    publisher = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        null=True, blank=True,
        verbose_name=_("Publisher"))
    date_published = models.DateField(
        null=True, blank=True,
        default=timezone.now,
        verbose_name=_('Published date'))
    permalink = models.URLField(
        null=True, blank=True,
        verbose_name=_('URL'))
    attachment = models.ForeignKey(
        Document, null=True, blank=True,
        on_delete=models.SET_NULL)

    def __str__(self):
        return self.title
