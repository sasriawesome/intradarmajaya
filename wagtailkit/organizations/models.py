from django.db import models
from django.utils import translation

from mptt.models import MPTTModel, TreeForeignKey
from wagtail.search import index
from wagtail.documents.models import Document
from wagtailkit.core.models import MAX_LEN_MEDIUM, MAX_LEN_LONG, CreatorModelMixin, KitBaseModel

_ = translation.gettext_lazy


class DepartmentManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset().select_related('parent')
        return qs


class Department(CreatorModelMixin, MPTTModel, KitBaseModel):
    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')

    objects = DepartmentManager()

    parent = TreeForeignKey(
        'Department', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='department_upline',
        verbose_name=_('Upline'))
    code = models.CharField(
        unique=False,
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_('Code'))
    name = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_('Name'))

    autocomplete_search_field = 'name'

    def autocomplete_label(self):
        return self.name

    def __str__(self):
        return self.name

    def get_manager_position(self):
        staffs = getattr(self, 'staffs', None)
        return None if not staffs else staffs.filter(is_manager=True).first()

    def get_co_manager_position(self):
        staffs = getattr(self, 'staffs', None)
        return None if not staffs else staffs.filter(is_co_manager=True).first()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class PositionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('department', 'parent')


class Position(MPTTModel, KitBaseModel):
    class Meta:
        verbose_name = _('Position')
        verbose_name_plural = _('Positions')

    objects = PositionManager()

    parent = TreeForeignKey(
        'organizations.Position',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='chair_upline',
        verbose_name=_('Upline'))
    name = models.CharField(
        max_length=MAX_LEN_MEDIUM,
        verbose_name=_('Name'))
    department = TreeForeignKey(
        Department, related_name='staffs',
        on_delete=models.PROTECT,
        verbose_name=_('Department'))
    is_manager = models.BooleanField(
        default=False, verbose_name=_('Is Manager'))
    is_co_manager = models.BooleanField(
        default=False, verbose_name=_('Is Co-Manager'))
    is_active = models.BooleanField(
        default=True, verbose_name=_('Is Active'))
    employee_required = models.IntegerField(
        default=1, verbose_name=_('Employee required'))
    attachment = models.ForeignKey(
        Document, null=True, blank=True,
        on_delete=models.SET_NULL)

    # wagtail autocomplete
    autocomplete_search_field = 'name'

    def autocomplete_label(self):
        return "{}{}".format('--' * self.level,self.name)

    def get_strips(self):
        return '---' * self.level

    def get_active_chairman(self, max_person=5):
        chairmans = getattr(self, 'chairmans', None)
        if not chairmans:
            return None
        if self.is_manager or self.is_co_manager:
            return chairmans.filter(is_active=True).first()
        else:
            return chairmans.filter(is_active=True)[0:max_person]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
