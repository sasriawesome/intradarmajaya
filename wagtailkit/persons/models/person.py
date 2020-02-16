import uuid
from django.db import models, transaction
from django.utils import translation, timezone, text
from django.conf import settings

from wagtail.core.models import Orderable, ClusterableModel
from wagtail.search import index
from modelcluster.fields import ParentalKey

from wagtailkit.core.models import MAX_LEN_MEDIUM, KitBaseModel
from wagtailkit.numerators.models import NumeratorMixin
from .extra import Address, ContactInfo, KKNILevel

_ = translation.gettext_lazy


class PersonManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def get_employee(self):
        return self.filter(employee__isnull=False)

    def get_customer(self):
        return self.filter(partners__is_customer=True)

    def get_vendor(self):
        return self.filter(partners__is_vendor=True)

    def get_by_natural_key(self, inner_id):
        return self.get(inner_id=inner_id)


class Person(index.Indexed, ClusterableModel, NumeratorMixin, ContactInfo, KitBaseModel):
    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        permissions = (
            ('export_person', 'Can export Person'),
            ('import_person', 'Can import Person'),
            ('change_status_person', 'Can change status Person')
        )

    MALE = 'M'
    FEMALE = 'F'
    GENDER = (
        (MALE, _('Male')),
        (FEMALE, _('Female'))
    )
    objects = PersonManager()

    doc_code = 'PRS'

    show_title = models.BooleanField(
        default=False,
        verbose_name=_('Show title'),
        help_text=_('Show Mr or Mrs in front of name'))
    show_name_only = models.BooleanField(
        default=False,
        verbose_name=_('Show name only'),
        help_text=_('Show name only without academic title'))
    title = models.CharField(
        null=True, blank=True,
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Title"))
    fullname = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Full name"))
    nickname = models.CharField(
        null=True, blank=True,
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Nick name"))
    front_title = models.CharField(
        null=True, blank=True,
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Front title"),
        help_text=_("Academic title prefix, eg: Dr or Prof. Dr"))
    back_title = models.CharField(
        null=True, blank=True,
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Back title"),
        help_text=_("Academic title suffix, eg: Phd"))
    gender = models.CharField(
        max_length=1,
        choices=GENDER,
        default=MALE,
        verbose_name=_('Gender'))
    religion = models.CharField(
        null=True, blank=True,
        max_length=255,
        verbose_name=_('Religion'))
    nation = models.CharField(
        null=True, blank=True,
        max_length=255,
        verbose_name=_('Nation'))
    date_of_birth = models.DateField(
        null=True, blank=True,
        default=timezone.now,
        verbose_name=_('Date of birth'))
    place_of_birth = models.CharField(
        null=True, blank=True,
        max_length=255,
        verbose_name=_('Place of birth'))

    # Last Education
    last_education_level = models.CharField(
        max_length=5,
        choices=[(str(lvl.value), str(lvl.name)) for lvl in KKNILevel],
        default=KKNILevel.SMA.value,
        verbose_name=_('Level'))
    last_education_institution = models.CharField(
        null=True, blank=True,
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_('Institution'))
    last_education_name = models.CharField(
        null=True, blank=True,
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_('Major'))
    year_graduate = models.CharField(
        null=True, blank=True,
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_('Year graduate'))


    # SOCIALMEDIA
    facebook = models.URLField(
        null=True, blank=True,
        help_text=_('Facebook page URL'))
    twitter = models.CharField(
        null=True, blank=True,
        max_length=255,
        help_text=_('twitter username, without the @'))
    instagram = models.CharField(
        null=True, blank=True,
        max_length=255,
        help_text=_('Instagram username, without the @'))
    youtube = models.URLField(
        null=True, blank=True,
        help_text=_('YouTube channel or user account URL'))

    user_account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('User account'))

    is_employee_applicant = models.BooleanField(default=False, verbose_name=_('Employee applicant'))
    is_partner_applicant = models.BooleanField(default=False, verbose_name=_('Partner applicant'))
    is_matriculant = models.BooleanField(default=False, verbose_name=_('Matriculant'))

    search_fields = [
        index.SearchField('fullname', partial_match=True),
    ]

    # wagtail autocomplete
    autocomplete_search_field = 'fullname'

    def autocomplete_label(self):
        return "{} | {}".format(self.inner_id, self.fullname_with_title)

    @property
    def fullname_with_title(self):
        name = []
        if self.title and self.show_title:
            name.append(self.title)
        if self.front_title and not self.show_name_only:
            name.append(str(self.front_title) + '.')
        if self.fullname:
            name.append(self.fullname)
        if self.back_title and not self.show_name_only:
            name.append(', ' + str(self.back_title))
        return " ".join(name)

    def __str__(self):
        return str(self.fullname_with_title)

    def natural_key(self):
        key = (self.inner_id,)
        return key

    def save(self, force_insert=False, force_update=False,
             using=None,
             update_fields=None):
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using, update_fields=update_fields)

    @property
    def is_user(self):
        user = self.user_account
        return bool(user)

    def is_employee(self):
        employee = getattr(self, 'employee', None)
        if employee:
            employee = employee.is_active
        return bool(employee)

    def is_teacher(self):
        teacher = getattr(self, 'teacher', None)
        if teacher:
            teacher = teacher.is_active
        return bool(teacher)

    def is_student(self):
        student = getattr(self, 'student', None)
        if student:
            student = student.is_active
        return bool(student)

    def is_partner(self):
        partner = getattr(self, 'partner', None)
        if partner:
            partner = partner.is_active
        return bool(partner)

    def is_customer(self):
        partner = getattr(self, 'partner', None)
        customer = None
        if partner:
            customer = partner.is_active and partner.is_customer
        return bool(customer)

    def is_supplier(self):
        partner = getattr(self, 'partner', None)
        supplier = None
        if partner:
            supplier = partner.is_active and partner.is_supplier
        return bool(supplier)

    def is_vendor(self):
        partner = getattr(self, 'partner', None)
        vendor = None
        if partner:
            vendor = partner.is_active and partner.is_vendor
        return bool(vendor)

    def get_last_education_level_display(self):
        return KKNILevel(self.last_education_level).name

    def create_user_account(self, username=None, password=None):
        if not self.user_account:
            with transaction.atomic():
                usermodel = settings.AUTH_USER_MODEL
                username = username if username else text.slugify(
                    self.fullname)
                password = password if password else 'default_pwd'
                new_user = usermodel.objects.create_user(
                    username=username,
                    password=password,
                    is_staff=False
                )
                self.user_account = new_user
                self.save()

    def bind_user_account(self, user):
        with transaction.atomic():
            self.user_account = user
            self.save()


class PersonAddress(Orderable, Address, KitBaseModel):
    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Address')

    person = ParentalKey(
        Person, on_delete=models.CASCADE,
        related_name='address',
        verbose_name=_("Person"))
    is_primary = models.BooleanField(
        default=True, verbose_name=_('Primary'))
    name = models.CharField(
        null=True, blank=False,
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_("Name"), help_text=_('E.g. Home Address or Office Address'))
