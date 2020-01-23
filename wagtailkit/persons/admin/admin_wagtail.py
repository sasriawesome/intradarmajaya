from django.contrib.admin.utils import quote, capfirst
from django.conf.urls import url
from django.shortcuts import get_object_or_404, reverse
from django.utils.translation import gettext_lazy as _

from wagtail.admin import messages
from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel,
    TabbedInterface, ObjectList)
from wagtail.documents.edit_handlers import DocumentChooserPanel

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin.views import IndexView, ModelFormView

from wagtailkit.admin.helpers import ButtonHelper, AdminURLHelper
from wagtailkit.printpdf.admin import PrintPDFModelAdminMixin
from wagtailkit.printpdf.helpers import PrintPDFButtonHelperMixin
from wagtailkit.importexport.admin import ImportExportModelAdminMixin
from wagtailkit.importexport.views import ImportExportIndexView
from wagtailkit.importexport.helpers import ImportExportAdminURLHelperMixin

from wagtailkit.persons.models import Person, PersonSettings
from wagtailkit.persons.resources import PersonResource


class PersonButtonHelper(PrintPDFButtonHelperMixin, ButtonHelper):
    """ Person buttin helper, with print detail """
    buttons_exclude = []


class AccountPersonalEditView(ModelFormView):
    """ Account Setting Personal data """

    instance_pk = None
    instance = None
    page_title = _('Update')

    def __init__(self, model_admin, instance_pk):
        super().__init__(model_admin)
        self.instance_pk = instance_pk
        self.pk_quoted = self.instance_pk
        self.instance = get_object_or_404(model_admin.model, pk=instance_pk)

    def get_page_subtitle(self):
        return self.instance

    def get_context_data(self, **kwargs):
        context = {'instance': self.instance}
        context.update(kwargs)
        return super().get_context_data(**context)

    def get_template_names(self):
        return self.model_admin.get_edit_template()

    def get_success_url(self):
        return self.url_helper.get_action_url('account_personal_edit')

    def get_success_message(self, instance):
        return _("%(model_name)s '%(instance)s' updated.") % {
            'model_name': capfirst(self.opts.verbose_name), 'instance': instance
        }

    def get_success_message_buttons(self, instance):
        button_url = self.url_helper.get_action_url('account_personal_edit')
        return [messages.button(button_url, _('Update'))]


class PersonIndexView(ImportExportIndexView, IndexView):
    def get_context_data(self, **kwargs):
        context = {
            'is_searching': True if kwargs['req'].GET.get('q') else False
        }
        context.update(**kwargs)
        return super().get_context_data(**context)

    def get(self, request, *args, **kwargs):
        kwargs['req'] = request
        return super().get(request, *args, **kwargs)


class PersonAdminURLHelper(ImportExportAdminURLHelperMixin, AdminURLHelper):
    pass


class PersonModelAdmin(ImportExportModelAdminMixin, PrintPDFModelAdminMixin, ModelAdmin):
    model = Person
    resource_class = PersonResource
    menu_icon = 'fa-user'
    menu_label = _('Persons')
    search_fields = [
        'fullname',
        'user_account__first_name',
        'user_account__last_name', ]
    list_display = [
        'fullname_with_title',
        'is_user_label',
        'is_employee_label',
        'is_partner_label',
        'date_created']
    button_helper_class = PersonButtonHelper
    url_helper_class = PersonAdminURLHelper
    inspect_view_enabled = True
    index_view_class = PersonIndexView
    account_personal_edit_view_class = AccountPersonalEditView

    profile_panels = [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('show_title'),
                FieldPanel('show_name_only'),
            ]),
            FieldPanel('title'),
            FieldPanel('front_title'),
            FieldPanel('back_title'),
            FieldPanel('fullname'),
            FieldPanel('gender'),
            FieldPanel('date_of_birth'),
            FieldPanel('place_of_birth'),
            FieldPanel('religion'),
            FieldPanel('nation')
        ], heading=_('Name')),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('phone1'),
                FieldPanel('phone2'),
            ]),
            FieldRowPanel([
                FieldPanel('email'),
                FieldPanel('website'),
            ]),
        ], heading=_('Contact Info')),

        InlinePanel(
            'address', heading=_('Address'),
            panels=[
                FieldPanel('is_primary'),
                FieldPanel('name', classname=' required'),
                FieldPanel('street1'),
                FieldPanel('street2'),
                FieldRowPanel([
                    FieldPanel('city'),
                    FieldPanel('province'),
                ]),
                FieldRowPanel([
                    FieldPanel('country'),
                    FieldPanel('zipcode'),
                ]),
            ],
            label=_('Address'), max_num=3,
        ),
    ]

    formal_education_history_panels = InlinePanel(
        'education_histories', heading=_('Education Histories'),
        panels=[
            FieldRowPanel([
                FieldPanel('institution_name'),
                FieldPanel('level'),
            ]),
            FieldRowPanel([
                FieldPanel('major'),
                FieldPanel('status'),
            ]),
            FieldRowPanel([
                FieldPanel('date_start'),
                FieldPanel('date_end'),
            ]),
            DocumentChooserPanel('attachment')
        ],
        label=_('Education History')
    )

    nonformal_education_history_panels = InlinePanel(
        'nonformaleducation_histories', heading=_('Non Formal Education Histories'),
        panels=[
            FieldPanel('name'),
            FieldPanel('institution_name'),
            FieldPanel('description'),
            FieldRowPanel([
                FieldPanel('date_start'),
                FieldPanel('date_end'),
            ]),
            FieldPanel('status'),
            DocumentChooserPanel('attachment')

        ],
        label=_('Education History'),
    )

    skils_panel = InlinePanel(
        'skill_sets', heading=_('Skills'),
        panels=[
            MultiFieldPanel([
                FieldPanel('name'),
                FieldPanel('description'),
                FieldPanel('level'),
            ])
        ],
        label=_('Skill'),
    )

    awards_panel = InlinePanel(
        'awards', heading=_('Awards'),
        panels=[
            FieldPanel('name'),
            FieldPanel('description'),
            FieldPanel('date'),
            DocumentChooserPanel('attachment')
        ],
        label=_('Award'),
    )

    family_panel = InlinePanel(
        'families', heading=_('Family'),
        panels=[
            MultiFieldPanel([
                FieldPanel('relation'),
                FieldPanel('relationship'),
                FieldPanel('name'),
                FieldPanel('date_of_birth'),
                FieldPanel('place_of_birth'),
                FieldPanel('job'),
                FieldPanel('address'),
            ])
        ],
        label=_('Family'),
    )

    publications_panel = InlinePanel(
        'publications', heading=_('Publications'),
        panels=[
            MultiFieldPanel([
                FieldPanel('title'),
                FieldPanel('description'),
                FieldPanel('publisher'),
                FieldPanel('date_published'),
                FieldPanel('permalink'),
                DocumentChooserPanel('attachment')
            ])
        ],
        label=_('Publication'),
    )

    working_history_panel = InlinePanel(
        'working_histories', heading=_('Working Histories'),
        panels=[
            FieldPanel('institution_name'),
            FieldPanel('department'),
            FieldRowPanel([
                FieldPanel('position'),
                FieldPanel('status'),
            ]),
            FieldRowPanel([
                FieldPanel('date_start'),
                FieldPanel('date_end'),
            ]),
            DocumentChooserPanel('attachment')
        ],
        label=_('Working History'),
    )

    organization_history_panels = InlinePanel(
        'organization_histories', heading=_('Organization Histories'),
        panels=[
            FieldPanel('organization'),
            FieldRowPanel([
                FieldPanel('position'),
                FieldPanel('status'),
            ]),
            FieldPanel('description'),
            FieldRowPanel([
                FieldPanel('date_start'),
                FieldPanel('date_end'),
            ]),
            DocumentChooserPanel('attachment')
        ],
        label=_('Organization History'),
    )

    social_panels = [
        MultiFieldPanel([
            FieldPanel('facebook'),
            FieldPanel('twitter'),
            FieldPanel('instagram'),
            FieldPanel('youtube'),
        ], heading=_('Social Media Account')),
    ]

    account_panels = [
        MultiFieldPanel([
            FieldPanel('user_account'),
        ], heading=_('Account')),
    ]

    def is_user_label(self, obj):
        return obj.is_user

    def is_employee_label(self, obj):
        return bool(obj.is_employee)

    def is_partner_label(self, obj):
        return obj.is_partner

    is_user_label.boolean = True
    is_employee_label.boolean = True
    is_partner_label.boolean = True
    is_user_label.short_description = _("User")
    is_employee_label.short_description = _("Employee")
    is_partner_label.short_description = _("Partner")

    def get_edit_handler(self, instance, request):

        setting = PersonSettings.for_site(request.site)

        edit_handler = [
            ObjectList(self.profile_panels, heading=_('Profile')),
        ]

        history_panels = []

        if setting.show_skill:
            history_panels.append(self.skils_panel)

        if setting.show_award:
            history_panels.append(self.awards_panel)

        if setting.show_publication:
            history_panels.append(self.publications_panel)

        if setting.show_formal_education_history:
            history_panels.append(self.formal_education_history_panels)

        if setting.show_nonformal_education_history:
            history_panels.append(self.nonformal_education_history_panels)

        if setting.show_working_history:
            history_panels.append(self.working_history_panel)

        if setting.show_organization_history:
            history_panels.append(self.organization_history_panels)

        if setting.show_histories_tab and history_panels:
            edit_handler.append(ObjectList(history_panels, heading=_('Histories')))

        edit_handler.append(ObjectList(self.social_panels, heading=_('Social')))

        if setting.show_family:
            edit_handler.append(ObjectList([self.family_panel], heading=_('Family')))

        if request.user.is_superuser:
            edit_handler = edit_handler + [
                ObjectList(self.account_panels, heading='Account')
            ]

        return TabbedInterface(edit_handler)

    def account_personal_edit_view(self, request):
        user_fullname = request.user.get_full_name()
        fullname = (request.user.username if not user_fullname else user_fullname)
        instance, created = self.model.objects.get_or_create(
            user_account=request.user, defaults={
                'fullname': fullname
            }
        )
        kwargs = {'model_admin': self, 'instance_pk': instance.id}
        view_class = self.account_personal_edit_view_class
        return view_class.as_view(**kwargs)(request)

    def get_admin_urls_for_registration(self):
        urls = super().get_admin_urls_for_registration()
        account_personal_edit_url = (
            url(r'^account/person/$',
                self.account_personal_edit_view,
                name=self.url_helper.get_action_url_name('account_personal_edit')),
        )
        return account_personal_edit_url + urls


modeladmin_register(PersonModelAdmin)
