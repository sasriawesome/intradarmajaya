import os
import uuid

from django.db import models
from django.utils import timezone, translation
from wagtail.contrib.settings.models import BaseSetting
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList, FieldPanel, MultiFieldPanel, FieldRowPanel
from wagtail.contrib.settings.registry import register_setting
from wagtail.admin.edit_handlers import RichTextField

from import_export.formats.base_formats import DEFAULT_FORMATS

_ = translation.gettext_lazy


def get_choices():
    choices = []
    for i, f in enumerate(DEFAULT_FORMATS):
        choices.append((str(i), f().get_title(),))
    return choices


def upload_import_file_to(instance, filename):
    filename, ext = os.path.splitext(filename)
    return os.path.join(
        'import_export',
        'import_export_{uuid}_{filename}{ext}'.format(
            uuid=uuid.uuid4(), filename=filename, ext=ext)
    )


class ImportExportHistoryAbstract(models.Model):
    class Meta:
        abstract = True

    date_created = models.DateTimeField(
        default=timezone.now, verbose_name=_('Date created'))
    formats = models.CharField(
        choices=get_choices, verbose_name=_('formats'))
    file = models.FileField(
        verbose_name=_('file'),
        upload_to=upload_import_file_to,
        blank=True)

    edit_handler = [
        ObjectList([
            MultiFieldPanel([
                FieldPanel('formats'),
                FieldPanel('file'),
            ])
        ])
    ]


class ImportExportSetting(BaseSetting):

    class Meta:
        verbose_name = _('Import Export')
        verbose_name_plural = _('Import Exports')

    export_csv = models.BooleanField(
        default=True,
        verbose_name=_('Export as CSV file'))
    export_xls = models.BooleanField(
        default=True,
        verbose_name=_('Export as XLS file'))
    export_xlsx = models.BooleanField(
        default=True,
        verbose_name=_('Export as XLSX file'))
    export_json = models.BooleanField(
        default=True,
        verbose_name=_('Export as JSON file'))

    import_csv = models.BooleanField(
        default=True,
        verbose_name=_('Import as CSV file'))
    import_xls = models.BooleanField(
        default=True,
        verbose_name=_('Import as XLS file'))
    import_xlsx = models.BooleanField(
        default=True,
        verbose_name=_('Import as XLSX file'))
    import_json = models.BooleanField(
        default=True,
        verbose_name=_('Import as JSON file'))

    import_panels = [
        MultiFieldPanel([
            FieldPanel('import_csv'),
            FieldPanel('import_xls'),
            FieldPanel('import_xlsx'),
            FieldPanel('import_json'),
        ], heading=_('Formats'))
    ]
    export_panels = [
        MultiFieldPanel([
            FieldPanel('export_csv'),
            FieldPanel('export_xls'),
            FieldPanel('export_xlsx'),
            FieldPanel('export_json'),
        ], heading=_('Formats'))
    ]
    edit_handler = TabbedInterface([
        ObjectList(
            import_panels, heading=_('Import'),
            help_text=_('Import setting')),
        ObjectList(
            export_panels, heading=_('Export'),
            help_text=_('Export setting')),
    ])


register_setting(ImportExportSetting, icon='fa-upload')