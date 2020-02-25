from django.contrib.admin.utils import quote, capfirst
from django.conf.urls import url
from django.shortcuts import get_object_or_404, reverse
from django.utils.translation import gettext_lazy as _

from wagtail.admin import messages
from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel,
    TabbedInterface, ObjectList)
from wagtail.documents.edit_handlers import DocumentChooserPanel

from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from wagtail.contrib.modeladmin.views import IndexView, ModelFormView, InspectView

from wagtailkit.admin.helpers import ButtonHelper, AdminURLHelper
from wagtailkit.printpdf.admin import PrintPDFModelAdminMixin
from wagtailkit.printpdf.helpers import PrintPDFButtonHelperMixin
from wagtailkit.importexport.admin import ImportExportModelAdminMixin
from wagtailkit.importexport.views import ImportExportIndexView
from wagtailkit.importexport.helpers import ImportExportAdminURLHelperMixin

from wagtailkit.persons.models import Person
from wagtailkit.persons.resources import PersonResource

from intranet.humanresource.models import PersonSettings


class PersonButtonHelper(PrintPDFButtonHelperMixin, ButtonHelper):
    """ Person button helper, with print detail """
    buttons_exclude = []


class ProfileView(InspectView):
    page_title = _('Preview')
    template_name = 'modeladmin/persons/person/profile.html'

    def get_template_names(self):
        return self.template_name

    def check_action_permitted(self, user):
        return True


class AccountPersonalEditView(ModelFormView):
    """ Account Setting Personal data """

    instance_pk = None
    instance = None
    page_title = _('Update')
    edit_handler = None

    def __init__(self, model_admin, instance_pk, page_title=None, edit_handler=None):
        super().__init__(model_admin)
        self.instance_pk = instance_pk
        self.pk_quoted = self.instance_pk
        self.instance = get_object_or_404(model_admin.model, pk=instance_pk)
        self.page_title = page_title
        self.edit_handler = edit_handler

    def get_page_subtitle(self):
        return self.instance

    def get_edit_handler(self):
        return self.edit_handler.bind_to(self.model)

    def get_context_data(self, **kwargs):
        context = {'instance': self.instance}
        context.update(kwargs)
        return super().get_context_data(**context)

    def get_template_names(self):
        return self.model_admin.get_edit_template()

    def get_success_url(self):
        return self.url_helper.get_action_url('account_profile_page')

    def get_success_message(self, instance):
        return _("%(model_name)s '%(instance)s' updated.") % {
            'model_name': capfirst(self.opts.verbose_name), 'instance': instance
        }

    def get_success_message_buttons(self, instance):
        button_url = reverse('wagtailadmin_account')
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
    menu_icon = 'fa-user-circle'
    menu_label = _('Personals')
    search_fields = [
        'fullname',
        'user_account__first_name',
        'user_account__last_name', ]
    list_filter = ['date_created']
    list_display = [
        'inner_id',
        'fullname_with_title',
        'gender',
        'date_created']
    list_per_page = 20
    button_helper_class = PersonButtonHelper
    url_helper_class = PersonAdminURLHelper
    inspect_view_enabled = True
    index_view_class = PersonIndexView
    account_personal_edit_view_class = AccountPersonalEditView

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

    def get_profile_edit_handler(self, instance, request):
        edit_handler = []
        name_panels = [
            MultiFieldPanel([
                FieldPanel('fullname'),
                FieldPanel('nickname')
            ]),
        ]
        profile_panels = [
            MultiFieldPanel([
                FieldRowPanel([
                    FieldPanel('front_title'),
                    FieldPanel('back_title'),
                ]),
                FieldRowPanel([
                    FieldPanel('title'),
                    FieldPanel('gender'),
                ]),
                FieldRowPanel([
                    FieldPanel('date_of_birth'),
                    FieldPanel('place_of_birth'),
                ]),
                FieldRowPanel([
                    FieldPanel('religion'),
                    FieldPanel('nation')
                ]),
            ]),
        ]
        edit_handler.append(ObjectList(name_panels, heading=_('Name')))
        edit_handler.append(ObjectList(profile_panels, heading=_('Personal')))
        return edit_handler

    def get_options_edit_handler(self, instance, request):
        edit_handler = []
        options_panels = [
            FieldPanel('show_title'),
            FieldPanel('show_name_only'),
        ]
        status_panel = [
            FieldPanel('is_employee_applicant'),
            FieldPanel('is_partner_applicant'),
            FieldPanel('is_matriculant'),
        ]
        account_panel = [
            FieldPanel('user_account')
        ]
        has_change_status_perm = self.permission_helper.user_has_specific_permission(request.user, 'change_status')
        if has_change_status_perm:
            options_panels += status_panel
        if request.user.is_superuser:
            options_panels += account_panel
        edit_handler.append(ObjectList([
            MultiFieldPanel(options_panels)
        ], heading=_('Options')))
        return edit_handler

    def get_address_edit_handler(self, instance, request):
        edit_handler = []
        address_panels = [
            InlinePanel(
                'address', max_num=3,
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
            )
        ]
        edit_handler.append(ObjectList(address_panels, heading=_('Addresses')))
        return edit_handler

    def get_educations_edit_handlers(self, instance, request):
        setting = PersonSettings.for_site(request.site)
        edit_handler = []
        last_education = [
            MultiFieldPanel([
                FieldPanel('last_education_level'),
                FieldPanel('last_education_institution'),
                FieldPanel('last_education_name'),
                FieldPanel('year_graduate'),
            ]),
        ]
        formal_education_panels = [
            InlinePanel(
                'education_histories',
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
            )
        ]
        nonformal_education_panels = [
            InlinePanel(
                'nonformaleducation_histories',
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
            )
        ]
        edit_handler.append(ObjectList(last_education, heading=_('Last Education')))
        if setting.show_formal_education_history:
            edit_handler.append(ObjectList(formal_education_panels, heading=_('Formal Education')))
        if setting.show_nonformal_education_history:
            edit_handler.append(ObjectList(nonformal_education_panels, heading=_('Non Formal Education')))
        return edit_handler

    def get_skills_award_edit_handlers(self, instance, request):
        edit_handler = []
        skils_panel = [
            InlinePanel(
                'skill_sets',
                panels=[
                    MultiFieldPanel([
                        FieldPanel('name'),
                        FieldPanel('description'),
                        FieldPanel('level'),
                    ])
                ],
            )
        ]
        awards_panel = [
            InlinePanel(
                'awards',
                panels=[
                    FieldPanel('name'),
                    FieldPanel('description'),
                    FieldPanel('date'),
                    DocumentChooserPanel('attachment')
                ],
            )
        ]
        publications_panel = [
            InlinePanel(
                'publications',
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
            )
        ]
        setting = PersonSettings.for_site(request.site)
        if setting.show_skill:
            edit_handler.append(ObjectList(skils_panel, heading=_('Skills')))
        if setting.show_award:
            edit_handler.append(ObjectList(awards_panel, heading=_('Awards')))
        if setting.show_publication:
            edit_handler.append(ObjectList(publications_panel, heading=_('Publications')))
        return edit_handler

    def get_working_organization_edit_handler(self, instance, request):
        edit_handler = []
        working_history_panel = [
            InlinePanel(
                'working_histories',
                panels=[
                    FieldPanel('institution_name'),
                    FieldPanel('department'),
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
            )
        ]
        organization_history_panels = [
            InlinePanel(
                'organization_histories',
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
            )
        ]
        setting = PersonSettings.for_site(request.site)
        if setting.show_working_history:
            edit_handler.append(ObjectList(working_history_panel, heading=_('Works')))
        if setting.show_organization_history:
            edit_handler.append(ObjectList(organization_history_panels, heading=_('Organizations')))
        return edit_handler

    def get_family_edit_handler(self, instance, request):
        edit_handler = []
        family_panel = [
            InlinePanel(
                'families',
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
            )
        ]
        setting = PersonSettings.for_site(request.site)
        if setting.show_family:
            edit_handler = [ObjectList(family_panel, heading=_('Family'))]
        return edit_handler

    def get_contacts_edit_handler(self, instance, request):
        social_panels = [
            ObjectList([
                MultiFieldPanel([
                    FieldPanel('phone1'),
                    FieldPanel('whatsapp'),
                    FieldPanel('email'),
                    FieldPanel('website'),
                ]),
            ], heading=_('Contacts')),
            ObjectList([
                MultiFieldPanel([
                    FieldPanel('facebook'),
                    FieldPanel('twitter'),
                    FieldPanel('instagram'),
                    FieldPanel('youtube'),
                ]),
            ], heading=_('Social Media'))
        ]
        return social_panels

    def get_edit_handler(self, instance, request):
        edit_handler = TabbedInterface([
            ObjectList([
                *self.get_profile_edit_handler(instance, request),
                *self.get_contacts_edit_handler(instance, request),
                *self.get_address_edit_handler(instance, request)
            ], heading=_('Personal')),
            ObjectList([
                *self.get_educations_edit_handlers(instance, request),
                *self.get_working_organization_edit_handler(instance, request),
            ], heading=_('Experiences')),
            ObjectList([
                *self.get_skills_award_edit_handlers(instance, request),
            ], heading=_('Skills & Awards')),
            ObjectList([
                *self.get_family_edit_handler(instance, request),
            ], heading=_('Relationships')),
            *self.get_options_edit_handler(instance, request)
        ])
        return edit_handler

    def get_instance(self, request):
        user_fullname = request.user.get_full_name()
        fullname = (request.user.username if not user_fullname else user_fullname)
        instance, created = self.model.objects.get_or_create(
            user_account=request.user, defaults={
                'fullname': fullname
            }
        )
        return instance

    def personal_edit_view(self, request):
        instance = self.get_instance(request)
        kwargs = {
            'page_title': _('Personal Info'),
            'model_admin': self,
            'instance_pk': instance.id,
            'edit_handler': ObjectList([
                *self.get_profile_edit_handler(instance, request),
            ])
        }
        view_class = self.account_personal_edit_view_class
        return view_class.as_view(**kwargs)(request)

    def education_edit_view(self, request):
        instance = self.get_instance(request)
        kwargs = {
            'page_title': _('Educations'),
            'model_admin': self,
            'instance_pk': instance.id,
            'edit_handler': ObjectList(self.get_educations_edit_handlers(instance, request))
        }
        view_class = self.account_personal_edit_view_class
        return view_class.as_view(**kwargs)(request)

    def skill_award_view(self, request):
        instance = self.get_instance(request)
        kwargs = {
            'page_title': _('Skills, Awards and Publications'),
            'model_admin': self,
            'instance_pk': instance.id,
            'edit_handler': ObjectList(self.get_skills_award_edit_handlers(instance, request))
        }
        view_class = self.account_personal_edit_view_class
        return view_class.as_view(**kwargs)(request)

    def contacts_account_view(self, request):
        instance = self.get_instance(request)
        kwargs = {
            'page_title': _('Contacts'),
            'model_admin': self,
            'instance_pk': instance.id,
            'edit_handler': ObjectList(self.get_contacts_edit_handler(instance, request))
        }
        view_class = self.account_personal_edit_view_class
        return view_class.as_view(**kwargs)(request)

    def working_organization_view(self, request):
        instance = self.get_instance(request)
        kwargs = {
            'page_title': _('Working and Organizations'),
            'model_admin': self,
            'instance_pk': instance.id,
            'edit_handler': ObjectList(self.get_working_organization_edit_handler(instance, request))
        }
        view_class = self.account_personal_edit_view_class
        return view_class.as_view(**kwargs)(request)

    def family_view(self, request):
        instance = self.get_instance(request)
        kwargs = {
            'page_title': _('Families'),
            'model_admin': self,
            'instance_pk': instance.id,
            'edit_handler': ObjectList(self.get_family_edit_handler(instance, request))
        }
        view_class = self.account_personal_edit_view_class
        return view_class.as_view(**kwargs)(request)

    def profile_page_view(self, request):
        instance = self.get_instance(request)
        kwargs = {'model_admin': self, 'instance_pk': str(instance.id)}
        return ProfileView.as_view(**kwargs)(request)

    def profile_pdf_view(self, request):
        instance = self.get_instance(request)
        kwargs = {'model_admin': self, 'instance_pk': str(instance.id)}
        view_class = self.detail_print_view_class
        return view_class.as_view(**kwargs)(request)

    def get_admin_urls_for_registration(self):
        urls = super().get_admin_urls_for_registration()
        account_personal_edit_url = (
            url(r'^account/person/$', self.personal_edit_view,
                name=self.url_helper.get_action_url_name('account_personal_edit')),
            url(r'^account/education/$', self.education_edit_view,
                name=self.url_helper.get_action_url_name('account_education_edit')),
            url(r'^account/skills_awards_publications/$', self.skill_award_view,
                name=self.url_helper.get_action_url_name('account_skill_edit')),
            url(r'^account/contacts_accounts/$', self.contacts_account_view,
                name=self.url_helper.get_action_url_name('account_contact_edit')),
            url(r'^account/working_organizations/$', self.working_organization_view,
                name=self.url_helper.get_action_url_name('account_working_edit')),
            url(r'^account/families/$', self.family_view,
                name=self.url_helper.get_action_url_name('account_family_edit')),
            url(r'^account/profile_page/$', self.profile_page_view,
                name=self.url_helper.get_action_url_name('account_profile_page')),
            url(r'^account/profile_pdf/$', self.profile_pdf_view,
                name=self.url_helper.get_action_url_name('account_profile_pdf')),
        )
        return account_personal_edit_url + urls

