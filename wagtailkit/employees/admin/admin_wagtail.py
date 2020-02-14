from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect, reverse, get_object_or_404
from django.conf.urls import url

from wagtail.admin import messages
from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel,
    TabbedInterface, ObjectList)
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.contrib.modeladmin.views import CreateView
from wagtail.contrib.modeladmin.helpers import PermissionHelper, ButtonHelper

from wagtailkit.admin.admin import ModelAdmin
from wagtailkit.autocompletes.edit_handlers import AutocompletePanel
from wagtailkit.persons.admin import PersonModelAdmin
from wagtailkit.employees.models import EmployeePersonal, Employee, Employment
from wagtailkit.printpdf.helpers import PrintPDFButtonHelperMixin, PrintPDFAdminURLHelperMixin
from wagtailkit.printpdf.admin import PrintPDFModelAdminMixin


class EmployeeButtonHelper(PrintPDFButtonHelperMixin, ButtonHelper):

    def get_buttons_for_obj(self, obj, exclude=None, classnames_add=None, classnames_exclude=None):
        btns = super().get_buttons_for_obj(obj, exclude, classnames_add, classnames_exclude)
        pk = obj.person.pk
        if exclude is None:
            exclude = []

        # user_has_perm = self.permission_helper.user_can_inspect_obj(self.request.user, obj)
        # if 'inspect_personal' not in exclude and obj and user_has_perm:
        #     btns.insert(1, self.create_custom_button('inspect_personal', pk, classnames_add, classnames_exclude))

        return btns


class EmployeAdminUrlHelper(PrintPDFAdminURLHelperMixin):
    pass


class EmployeeCreateView(CreateView):
    def get_instance(self):
        instance = super().get_instance()
        instance.creator = self.request.user
        return instance

    def form_valid(self, form):
        instance = form.save()
        messages.success(
            self.request, self.get_success_message(instance),
            buttons=self.get_success_message_buttons(instance)
        )
        return redirect(self.get_success_url())


class EmployeePermissionHelper(PermissionHelper):
    pass


class EmployeeModelAdmin(PrintPDFModelAdminMixin, ModelAdmin):
    model = Employee
    menu_label = _('Employee')
    menu_icon = ' icon-fa-user'
    search_fields = ['eid', 'person__fullname', 'position__name']
    list_filter = ['is_active', 'employment', 'person__last_education_level', 'date_registered', ]
    list_display = ['eid', 'person', 'position', 'date_registered']
    permission_helper_class = EmployeePermissionHelper
    button_helper_class = EmployeeButtonHelper
    url_helper_class = EmployeAdminUrlHelper
    create_view_class = EmployeeCreateView
    inspect_view_enabled = True

    employee_panels = [
        MultiFieldPanel([
            FieldPanel('eid'),
            AutocompletePanel('person'),
            AutocompletePanel('position'),
            FieldPanel('employment'),
            FieldPanel('date_registered'),
            DocumentChooserPanel('attachment'),
            FieldPanel('is_teacher_applicant'),
            FieldPanel('is_active'),
        ]),
        InlinePanel(
            'extra_positions', label=_('Extra Positions'),
            panels=[
                AutocompletePanel('position'),
                DocumentChooserPanel('attachment'),
                FieldPanel('is_active')
            ]
        )
    ]
    edit_handler = TabbedInterface([
        ObjectList(employee_panels, heading=_('Basic Information'))
    ])

    # def get_admin_urls_for_registration(self):
    #     urls = super().get_admin_urls_for_registration()
    #     if self.inspect_view_enabled:
    #         urls += (
    #             url(self.url_helper.get_action_url_pattern('inspect_personal'),
    #                 self.inspect_personal_view,
    #                 name=self.url_helper.get_action_url_name('inspect_personal')),
    #         )
    #     return urls
    #
    # def inspect_personal_view(self, request, instance_pk):
    #     employee_personal = get_object_or_404(klass=EmployeePersonal, pk=instance_pk)
    #     return redirect(reverse('employees_employeepersonal_modeladmin_inspect', args=(employee_personal.id,)))


class EmployeePersonalModelAdmin(PersonModelAdmin):
    model = EmployeePersonal
    menu_icon = 'fa-user'
    menu_label = _('Employee Personal')
    button_helper_class = ButtonHelper
    inspect_view_enabled = False


class EmploymentModelAdmin(ModelAdmin):
    model = Employment
    menu_icon = ' icon-fa-wpforms'
    menu_label = _('Employments')
    panels = [
        FieldPanel('name'),
        FieldPanel('note')
    ]
