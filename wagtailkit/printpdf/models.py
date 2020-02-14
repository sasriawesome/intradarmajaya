from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.settings.models import BaseSetting
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList, FieldPanel, MultiFieldPanel, FieldRowPanel
from wagtail.contrib.settings.registry import register_setting
from wagtail.admin.edit_handlers import RichTextField

html_content_cover = """
<h1>Awesome Company</h1>
<p>Made with taste<p/>
"""

html_content_header = """
    <h1>Awesome Company</h1>
    <p>Made with taste<p/>
"""

html_content_footer = """
    <p>Feel free to contact 24/7 always on.<p/>
"""


class PrintPDFSetting(BaseSetting):
    class Meta:
        verbose_name = _('PDF Print')

    menu_icon = 'icon-fa-printer'

    # Detail Document Settings
    index_orientation = models.CharField(
        max_length=50,
        choices=(('portrait', 'Portrait'), ('landscape', 'Landscape')),
        default='portrait',
        verbose_name=_('Orientation'),
        help_text=_('Document orientation'))
    index_paper_size = models.CharField(
        max_length=50,
        choices=(('A4', 'A4'), ('folio', 'Folio')),
        default='A4',
        verbose_name=_('Paper size'),
        help_text=_('Set document paper size'))
    index_show_cover = models.BooleanField(
        default=False,
        verbose_name=_('Show cover'),
        help_text=_('Show document cover'))
    index_show_header = models.BooleanField(
        default=True,
        verbose_name=_('Show header'),
        help_text=_('Show document header'))
    index_show_footer = models.BooleanField(
        default=True,
        verbose_name=_('Show footer'),
        help_text=_('Show document footer'))
    index_margin_top = models.IntegerField(
        default=45,
        verbose_name=_('Top'),
        help_text=_('Set index document top margin'))
    index_margin_bottom = models.IntegerField(
        default=25,
        verbose_name=_('Bottom'),
        help_text=_('Set index document bottom margin'))
    index_margin_left = models.IntegerField(
        default=25,
        verbose_name=_('Left'),
        help_text=_('Set index document left margin'))
    index_margin_right = models.IntegerField(
        default=25,
        verbose_name=_('Right'),
        help_text=_('Set index document right margin'))

    # Detail Document Settings
    detail_orientation = models.CharField(
        max_length=50,
        choices=(('portrait', 'Portrait'), ('landscape', 'Landscape')),
        default='portrait',
        verbose_name=_('Orientation'),
        help_text=_('Document orientation'))
    detail_paper_size = models.CharField(
        max_length=50,
        choices=(('A4', 'A4'), ('folio', 'Folio')),
        default='A4',
        verbose_name=_('Paper size'),
        help_text=_('Set document paper size'))
    detail_show_cover = models.BooleanField(
        default=True,
        verbose_name=_('Show cover'),
        help_text=_('Show document cover'))
    detail_show_header = models.BooleanField(
        default=True,
        verbose_name=_('Show header'),
        help_text=_('Show document header'))
    detail_show_footer = models.BooleanField(
        default=True,
        verbose_name=_('Show footer'),
        help_text=_('Show document footer'))
    detail_margin_top = models.IntegerField(
        default=45,
        verbose_name=_('Top'),
        help_text=_('Set index document top margin'))
    detail_margin_bottom = models.IntegerField(
        default=25,
        verbose_name=_('Bottom'),
        help_text=_('Set index document bottom margin'))
    detail_margin_left = models.IntegerField(
        default=25,
        verbose_name=_('Left'),
        help_text=_('Set index document left margin'))
    detail_margin_right = models.IntegerField(
        default=25,
        verbose_name=_('Right'),
        help_text=_('Set index document right margin'))

    custom_css = models.TextField(
        max_length=2000, null=True, blank=True,
        verbose_name=_('Custom CSS'),
        help_text=_('Add custom style to PDF'))
    content_cover = RichTextField(
        default=html_content_cover,
        max_length=2000, null=True, blank=True,
        verbose_name=_('Cover content'),
        help_text=_('Insert HTML content to document cover, use Custom CSS for better display'))
    content_header = RichTextField(
        default=html_content_header,
        max_length=2000, null=True, blank=True,
        verbose_name=_('Header content'),
        help_text=_('Insert HTML content to document header, use Custom CSS for better display'))
    content_footer = RichTextField(
        default=html_content_footer,
        max_length=2000, null=True, blank=True,
        verbose_name=_('Header content'),
        help_text=_('Insert HTML content to document footer, use Custom CSS for better display'))

    index_panels = [
        MultiFieldPanel([
            FieldPanel('index_paper_size'),
            FieldPanel('index_orientation'),
            FieldPanel('index_show_cover'),
            FieldPanel('index_show_header'),
            FieldPanel('index_show_footer'),
        ], heading=_('Document')),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('index_margin_top'),
                FieldPanel('index_margin_bottom'),
            ]),
            FieldRowPanel([
                FieldPanel('index_margin_left'),
                FieldPanel('index_margin_right'),
            ])
        ], heading=_('Margin'))
    ]

    detail_panels = [
        MultiFieldPanel([
            FieldPanel('detail_paper_size'),
            FieldPanel('detail_orientation'),
            FieldPanel('detail_show_cover'),
            FieldPanel('detail_show_header'),
            FieldPanel('detail_show_footer'),
        ], heading=_('Document')),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('detail_margin_top'),
                FieldPanel('detail_margin_bottom'),
            ]),
            FieldRowPanel([
                FieldPanel('detail_margin_left'),
                FieldPanel('detail_margin_right'),
            ])
        ], heading=_('Margin'))
    ]

    css_panels = [
        FieldPanel('custom_css'),
    ]

    content_panels = [
        FieldPanel('content_cover'),
        FieldPanel('content_header'),
        FieldPanel('content_footer')
    ]

    edit_handler = TabbedInterface([
        ObjectList(
            index_panels, heading=_('Index View'),
            help_text=_('Set PDF document for index or list view')),
        ObjectList(
            detail_panels, heading=_('Detail View'),
            help_text=_('Set PDF document for specific object or detail view')),
        ObjectList(content_panels, heading=_('Content')),
        ObjectList(css_panels, heading=_('Custom CSS')),
    ])


register_setting(PrintPDFSetting, icon='fa-print')
