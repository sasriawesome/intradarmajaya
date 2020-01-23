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


@hooks.register('after_create_user')
def create_user_personal_information(request, user):
    """ Create personal information for each New User created"""
    data = {
        'user_account': user,
        'fullname': user.get_full_name() or user.username
    }
    Person.objects.create(**data)


@hooks.register('register_admin_search_area')
def register_person_search_area():
    return PersonsSearchArea(
        _('Persons'), reverse('persons_person_modeladmin_index'),
        classnames='icon icon-group', order=10000)


@hooks.register('register_account_menu_item')
def register_user_personal_account_menu(request):
    return {
        'url': reverse('persons_person_modeladmin_account_personal_edit'),
        'label': _('Set Personal Info'),
        'help_text': _('Update your personal infomation.')
    }
