import calendar
import datetime

from django.apps import apps
from django.db import models
from django.utils import translation
from django.contrib.contenttypes.models import ContentType

_ = translation.gettext_lazy


class NumeratorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def get_by_natural_key(self, ctype, date_start, date_end):
        return self.get(
            ctype=ctype, date_start=date_start, date_end=date_end)


class Numerator(models.Model):
    """ ContentTypeCounter is used as autogenerated number register
        like autonumber for uuid based Model """

    class Meta:
        verbose_name = _('Numerator')
        verbose_name_plural = _('Numerators')
        unique_together = ('ctype', 'dtype', 'date_start', 'date_end')

    YEARLY = 'Y'
    MONTHLY = 'M'
    FIXED = 'F'
    DTYPE = (
        (YEARLY, _('Yearly')),
        (MONTHLY, _('Montly')),
        (FIXED, _('Fixed')),
    )

    objects = NumeratorManager()

    ctype = models.ForeignKey(
        ContentType, on_delete=models.CASCADE,
        verbose_name=_('Content type'))
    dtype = models.CharField(
        max_length=50, verbose_name=_('Counter period'))
    date_start = models.DateField(verbose_name=_('Date start'))
    date_end = models.DateField(verbose_name=_('Date end'))
    counter = models.PositiveIntegerField(
        default=0, verbose_name=_('Counter'))

    @staticmethod
    def get_instance(instance, model=None, custom_code=None):
        if model is None:
            model = instance._meta.model
        year = instance.date_created.year
        if instance.numbering == Numerator.YEARLY:
            date_type = Numerator.YEARLY
            date_start_month = 1
            date_end_month = 12
            last_day = calendar.monthlen(year, date_end_month)
        elif instance.numbering == Numerator.MONTHLY:
            date_type = Numerator.MONTHLY
            date_start_month = instance.date_created.month
            date_end_month = instance.date_created.month
            last_day = calendar.monthlen(year, date_end_month)
        else:
            date_type = custom_code
            year = 2000
            date_start_month = 1
            date_end_month = 1
            last_day = 1
        defaults = {
            'ctype': ContentType.objects.get_for_model(model),
            'dtype': date_type,
            'date_start': datetime.date(year, date_start_month, 1),
            'date_end': datetime.date(year, date_end_month, last_day)
        }
        ct_counter, created = Numerator.objects.get_or_create(**defaults, defaults=defaults)
        return ct_counter

    def __str__(self):
        return str(self.ctype)

    def natural_key(self):
        natural_key = (
            self.ctype, self.date_start, self.date_end)
        return natural_key

    def real_model(self):
        return apps.get_model(
            self.ctype.app_label, self.ctype.model)

    def increase_counter(self):
        self.counter += 1
        return self.counter

    def decrease_counter(self):
        i = 1 if self.counter > 0 else 0
        self.counter -= i
        return self.counter

    def reset_counter(self):
        self.counter = 0
        return self.counter

    def get_numbering(self):
        return Numerator.YEARLY


class NumeratorMixin(models.Model):
    """ Mixin for Numerator Model """

    class Meta:
        abstract = True

    ct_counter = None
    doc_code = 'IID'  # inner id code
    numbering = Numerator.YEARLY


    reg_number = models.PositiveIntegerField(
        null=True, blank=True, editable=False,
        verbose_name=_('Register number'))
    inner_id = models.CharField(
        unique=True, editable=False,
        null=True, blank=True,
        max_length=50,
        verbose_name=_('Inner ID'))

    def get_doc_code(self):
        return self.doc_code

    def generate_inner_id(self):
        """
            Generate human friendly document number,
            override this method to customize inner_id format
        """
        form = [
            self.get_doc_code(),
            self.date_created.strftime("%m%y"),
            str(self.reg_number).zfill(4)
        ]
        self.inner_id = '{}.{}.{}'.format(*form)
        return self.inner_id

    def get_counter(self):
        ct_counter = Numerator.get_instance(self)
        return ct_counter

    def register(self):
        """
        Register and get Numerator instance for
        this model, Get latest counter value and then
        generate and set inner_id
        """
        # Get Numerator instance for this model
        if self.ct_counter is None:
            self.ct_counter = self.get_counter()

        # If reg_number is None get new one
        if self.reg_number is None:
            self.reg_number = self.ct_counter.increase_counter()

        # If reg number > counter set new counter value
        if self.reg_number > self.ct_counter.counter:
            self.ct_counter.counter = self.reg_number

        return self.generate_inner_id()

    def save(self, *args, **kwargs):
        if self.ct_counter is None:
            self.register()
        self.ct_counter.save()

        super().save(*args, **kwargs)