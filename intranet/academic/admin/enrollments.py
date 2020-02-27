from django.utils.translation import gettext_lazy as _

from wagtail.admin.edit_handlers import (
    FieldPanel, MultiFieldPanel, InlinePanel,
    TabbedInterface, ObjectList)

from wagtailkit.admin.admin import ModelAdmin
from wagtailkit.autocompletes.edit_handlers import AutocompletePanel
from wagtailkit.enrollments.models import Enrollment


class EnrollmentModelAdmin(ModelAdmin):
    menu_label = _('Enrollments')
    menu_icon = 'fa-wpforms'
    model = Enrollment
    list_per_page = 20

    edit_handler = TabbedInterface([
        ObjectList([
            MultiFieldPanel([
                AutocompletePanel('student'),
                FieldPanel('academic_year'),
                FieldPanel('note'),
                FieldPanel('coach_review'),
                FieldPanel('status'),
            ])
        ], heading=_('Form')),
        ObjectList([
            InlinePanel( 'lectures', panels=[
                AutocompletePanel('lecture'),
                FieldPanel('criteria'),
            ])
        ], heading=_('Lectures'))
    ])


