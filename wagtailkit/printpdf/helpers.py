from django.utils.translation import gettext_lazy as _
from django.contrib.admin.utils import quote, capfirst
from django.shortcuts import reverse
from django.utils.functional import cached_property

from wagtail.contrib.modeladmin.helpers import AdminURLHelper
from wagtailkit.admin.helpers import ButtonHelper


class PrintPDFAdminURLHelperMixin(AdminURLHelper):
    def get_action_url_pattern(self, action):
        if action in ('create', 'choose_parent', 'index', 'print_index'):
            return self._get_action_url_pattern(action)
        return self._get_object_specific_action_url_pattern(action)

    def get_action_url(self, action, *args, **kwargs):
        if action in ('create', 'choose_parent', 'index', 'print_index'):
            return reverse(self.get_action_url_name(action))
        url_name = self.get_action_url_name(action)
        return reverse(url_name, args=args, kwargs=kwargs)

    @cached_property
    def print_index_url(self):
        return self.get_action_url('print_index')


class PrintPDFButtonHelperMixin(ButtonHelper):
    def get_buttons_for_obj(self, obj, exclude=None, classnames_add=None, classnames_exclude=None):
        btns = super().get_buttons_for_obj(obj, exclude, classnames_add, classnames_exclude)
        pk = getattr(obj, self.opts.pk.attname)
        if exclude is None:
            exclude = []
        if 'print_detail' not in exclude and obj and self.permission_helper.user_can_inspect_obj(self.request.user,
                                                                                                 obj):
            btns.append(self.create_custom_button('print_detail', pk, classnames_add, classnames_exclude))
        return btns
