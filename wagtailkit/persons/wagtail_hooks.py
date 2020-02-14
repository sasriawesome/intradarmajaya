from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from wagtail.core import hooks
from wagtail.admin.search import SearchArea
from wagtail.contrib.modeladmin.helpers import PermissionHelper

from wagtailkit.persons.models import Person


class PersonsSearchArea(SearchArea):
    permission_helper_class = PermissionHelper
    model = Person

    def get_permission_helper(self):
        return self.permission_helper_class(self.model)

    def is_shown(self, request):
        return self.get_permission_helper().user_has_any_permissions(request.user)

# TODO Autocreate Personal Information
# @hooks.register('after_create_user')
# def create_user_personal_information(request, user):
#     """ Create personal information for each New User created"""
#     data = {
#         'user_account': user,
#         'fullname': user.get_full_name() or user.username
#     }
#     Person.objects.create(**data)


@hooks.register('register_admin_search_area')
def register_person_search_area():
    return PersonsSearchArea(
        _('Persons'), reverse('persons_person_modeladmin_index'),
        classnames='icon icon-group', order=10000)

@hooks.register('register_account_menu_item')
def register_profile_page_menu(request):
    return {
        'url': reverse('persons_person_modeladmin_account_profile_page'),
        'label': _('Your Profile'),
        'help_text': _('Show detail profile.')
    }

@hooks.register('register_account_menu_item')
def register_user_personal_account_menu(request):
    return {
        'url': reverse('persons_person_modeladmin_account_personal_edit'),
        'label': _('Personal Info'),
        'help_text': _('Update your personal infomation.')
    }


@hooks.register('register_account_menu_item')
def register_contact_account_menu(request):
    return {
        'url': reverse('persons_person_modeladmin_account_contact_edit'),
        'label': _('Contacts'),
        'help_text': _('Update your contact and social accounts.')
    }


@hooks.register('register_account_menu_item')
def register_user_skills_menu(request):
    return {
        'url': reverse('persons_person_modeladmin_account_skill_edit'),
        'label': _('Skills, Awards and Publications'),
        'help_text': _('Update your personal skills, awards and publications.')
    }

@hooks.register('register_account_menu_item')
def register_education_histories_menu(request):
    return {
        'url': reverse('persons_person_modeladmin_account_education_edit'),
        'label': _('Educations'),
        'help_text': _('Update your education histories.')
    }

@hooks.register('register_account_menu_item')
def register_working_organization_menu(request):
    return {
        'url': reverse('persons_person_modeladmin_account_working_edit'),
        'label': _('Working and Organizations'),
        'help_text': _('Update your working and volunteer histories.')
    }

@hooks.register('register_account_menu_item')
def register_families_menu(request):
    return {
        'url': reverse('persons_person_modeladmin_account_family_edit'),
        'label': _('Families'),
        'help_text': _('Update your family informations.')
    }