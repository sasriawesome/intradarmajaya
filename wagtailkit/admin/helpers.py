from django.contrib.admin.utils import quote, capfirst
from django.utils.translation import gettext_lazy as _

from wagtail.contrib.modeladmin.helpers import (
    AdminURLHelper as AdminURLHelperBase,
    PermissionHelper as PermissionHelperBase,
    ButtonHelper as ButtonHelperBase
)


class AdminURLHelper(AdminURLHelperBase):
    """ Custom AdminURLHelper """


class PermissionHelper(PermissionHelperBase):
    """ Custom PermissionHelper """

    def user_can(self, codename, user, obj=None):
        perm_codename = self.get_perm_codename(codename)
        return self.user_has_specific_permission(user, perm_codename)

    def can_view_other(self, user):
        return self.user_can('viewother', user)

    def can_change_other(self, user):
        return self.user_can('changeother', user)

    def is_owner(self, user, obj):
        return obj.creator == user

    def is_owner_manager(self, user, obj):
        creator_manager_position = obj.creator.person.employee.position.get_ancestors(ascending=True)[0]
        user_position = user.person.employee.position
        return user_position == creator_manager_position

    def user_can_edit_obj(self, user, obj):
        return self.user_can('change', user)

    def user_can_inspect_obj(self, user, obj):
        return self.inspect_view_enabled and self.user_has_any_permissions(user)


class ButtonHelper(ButtonHelperBase):
    """ Custom ButtonHelper """

    def create_custom_button(self, codename, pk=None, classnames_add=None, classnames_exclude=None):
        if classnames_add is None:
            classnames_add = []
        if classnames_exclude is None:
            classnames_exclude = []
        classnames = self.default_button_classnames + classnames_add
        cn = self.finalise_classname(classnames, classnames_exclude)
        return {
            'url': self.url_helper.get_action_url(codename, quote(pk)),
            'label': capfirst(_(codename.replace('_', ' '))),
            'classname': cn,
            'title': _('%s this %s') % (codename, self.verbose_name,),
        }


class StatusButtonHelper(ButtonHelper):
    """ Model status custom button helper """

    buttons_exclude = []

    def get_buttons_for_obj(self, obj, exclude=None, classnames_add=None, classnames_exclude=None):
        exclude = [] if not exclude else exclude
        exclude = exclude + self.buttons_exclude
        classnames_add = [] if not classnames_add else classnames_add
        classnames_exclude = [] if not classnames_exclude else classnames_exclude
        ph = self.permission_helper
        usr = self.request.user
        pk = getattr(obj, self.opts.pk.attname)

        # add custom button
        btns = super().get_buttons_for_obj(obj, exclude, classnames_add, classnames_exclude)

        if 'trash' not in exclude and ph.user_can('trash', usr, obj) and obj.is_draft:
            btns.append(self.create_custom_button('trash', pk, classnames_add, classnames_exclude))

        if 'draft' not in exclude and ph.user_can('draft', usr, obj) and obj.is_trash:
            btns.append(self.create_custom_button('draft', pk, classnames_add, classnames_exclude))

        if 'validate' not in exclude and ph.user_can('validate', usr, obj) and obj.is_draft:
            btns.append(self.create_custom_button('validate', pk, classnames_add, classnames_exclude))

        if 'approve' not in exclude and ph.user_can('approve', usr, obj) and obj.is_valid:
            btns.append(self.create_custom_button('approve', pk, classnames_add, classnames_exclude))

        if 'reject' not in exclude and ph.user_can('reject', usr, obj) and obj.is_valid:
            btns.append(self.create_custom_button('reject', pk, classnames_add, classnames_exclude))

        if 'process' not in exclude and ph.user_can('process', usr, obj) and obj.is_approved:
            btns.append(self.create_custom_button('process', pk, classnames_add, classnames_exclude))

        if 'complete' not in exclude and ph.user_can('complete', usr, obj) and obj.is_processed:
            btns.append(self.create_custom_button('complete', pk, classnames_add, classnames_exclude))

        if 'close' not in exclude and ph.user_can('close', usr, obj) and obj.is_completed:
            btns.append(self.create_custom_button('close', pk, classnames_add, classnames_exclude))

        return btns

class FourStepStatusButtonHelper(ButtonHelper):
    """ Model status custom button helper """

    buttons_exclude = []

    def get_buttons_for_obj(self, obj, exclude=None, classnames_add=None, classnames_exclude=None):
        exclude = [] if not exclude else exclude
        exclude = exclude + self.buttons_exclude
        classnames_add = [] if not classnames_add else classnames_add
        classnames_exclude = [] if not classnames_exclude else classnames_exclude
        ph = self.permission_helper
        usr = self.request.user
        pk = getattr(obj, self.opts.pk.attname)

        # add custom button
        btns = super().get_buttons_for_obj(obj, exclude, classnames_add, classnames_exclude)

        if 'trash' not in exclude and ph.user_can('trash', usr, obj) and obj.is_draft:
            btns.append(self.create_custom_button('trash', pk, classnames_add, classnames_exclude))

        if 'draft' not in exclude and ph.user_can('draft', usr, obj) and obj.is_trash:
            btns.append(self.create_custom_button('draft', pk, classnames_add, classnames_exclude))

        if 'validate' not in exclude and ph.user_can('validate', usr, obj) and obj.is_draft:
            btns.append(self.create_custom_button('validate', pk, classnames_add, classnames_exclude))

        if 'process' not in exclude and ph.user_can('process', usr, obj) and obj.is_valid:
            btns.append(self.create_custom_button('process', pk, classnames_add, classnames_exclude))

        if 'complete' not in exclude and ph.user_can('complete', usr, obj) and obj.is_processed:
            btns.append(self.create_custom_button('complete', pk, classnames_add, classnames_exclude))

        return btns