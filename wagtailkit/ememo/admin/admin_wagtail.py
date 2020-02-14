from wagtailkit.admin.admin import ModelAdmin

from wagtail.contrib.modeladmin.options import modeladmin_register
from wagtail.admin.edit_handlers import ObjectList, FieldPanel, RichTextFieldPanel, MultiFieldPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from django_select2.forms import Select2MultipleWidget
from wagtailkit.ememo.models import Memo


class MemoModelAdmin(ModelAdmin):
    model = Memo
    inspect_view_enabled = True
    menu_icon = 'fa-envelope'
    edit_handler =ObjectList([
        MultiFieldPanel([
            FieldPanel('receiver', widget=Select2MultipleWidget()),
            FieldPanel('cc', widget=Select2MultipleWidget()),
            FieldPanel('title'),
            RichTextFieldPanel('body'),
            DocumentChooserPanel('attachment')
        ])
    ])

modeladmin_register(MemoModelAdmin)
