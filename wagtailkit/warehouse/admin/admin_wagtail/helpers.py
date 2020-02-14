from wagtailkit.admin.helpers import (
    PermissionHelper,
    ButtonHelper,
    StatusButtonHelper,
    FourStepStatusButtonHelper,
)
from wagtailkit.printpdf.helpers import PrintPDFButtonHelperMixin


class RequestOrderPermissionHelper(PermissionHelper):
    """ Request Order PermissionHelper """

    def user_can(self, codename, user, obj=None):
        perm_codename = self.get_perm_codename(codename)
        return self.user_has_specific_permission(user, perm_codename)

    def can_view_other(self, user):
        return self.user_can('viewother', user)

    def can_change_other(self, user):
        return self.user_can('changeother', user)

    def is_owner(self, user, obj):
        return False if not getattr(obj, 'creator', None) else obj.creator == user

    def is_owner_manager(self, user, obj):
        """ Check user is owner manager """
        # check user has employee object
        user_person = getattr(user, 'person', None)
        if not user_person:
            return False
        # check user has employee object
        user_employee = getattr(user_person, 'employee', None)
        if not user_employee:
            return False
        creator_manager_position = obj.creator.person.employee.position.get_ancestors(ascending=True)[0]
        return user_employee.position == creator_manager_position

    def user_can_edit_obj(self, user, obj):
        can_change = self.user_can('change', user)
        can_change_other = self.user_can('changeother', user)
        is_editable = getattr(obj, 'is_editable', None)
        valid_owner = self.is_owner(user, obj) or self.is_owner_manager(user, obj)
        if user.is_superuser:
            return True
        if can_change_other and is_editable:
            return True
        if valid_owner and can_change and is_editable:
            return True
        else:
            return False

    def user_can_inspect_obj(self, user, obj):
        has_perm = self.inspect_view_enabled and self.user_has_any_permissions(user)
        can_view_other = self.user_can('viewother', user, obj)
        valid_owner = self.is_owner(user, obj) or self.is_owner_manager(user, obj)
        if user.is_superuser:
            return True
        if can_view_other and has_perm:
            return True
        if valid_owner and has_perm:
            return True
        else:
            return False

    def user_can_validate_obj(self, user, obj):
        has_perm = self.user_can('validate', user, obj)
        can_view_other = self.user_can('viewother', user, obj)
        valid_owner = self.is_owner(user, obj) or self.is_owner_manager(user, obj)
        if user.is_superuser:
            return True
        if can_view_other and has_perm:
            return True
        if valid_owner and has_perm:
            return True
        else:
            return False


class ProductTransferPermissionHelper(PermissionHelper):
    """ Request Order PermissionHelper """

    def user_can_edit_obj(self, user, obj):
        can_change = self.user_can('change', user)
        is_editable = getattr(obj, 'is_editable', None)
        if user.is_superuser:
            return True
        if can_change and is_editable:
            return True
        else:
            return False


class ProductTransferButtonHelper(PrintPDFButtonHelperMixin, FourStepStatusButtonHelper):
    buttons_exclude = ['approve', 'reject']


class RequestOrderButtonHelper(PrintPDFButtonHelperMixin, StatusButtonHelper):
    buttons_exclude = ['process', 'complete', 'close']


class AdjustmentButtonHelper(PrintPDFButtonHelperMixin, ButtonHelper):
    """ Stock adjusment button helper """

    buttons_exclude = []

    def get_buttons_for_obj(self, obj, exclude=None, classnames_add=None, classnames_exclude=None):
        exclude = [] if not exclude else exclude
        exclude = exclude + self.buttons_exclude
        classnames_add = [] if not classnames_add else classnames_add
        classnames_exclude = [] if not classnames_exclude else classnames_exclude
        usr = self.request.user
        ph = self.permission_helper
        pk = getattr(obj, self.opts.pk.attname)
        user_can_reconcile = ph.user_can('reconcile', usr, obj)

        # add custom button
        btns = super().get_buttons_for_obj(obj, exclude, classnames_add, classnames_exclude)

        if 'validate' not in exclude and ph.user_can('validate', usr, obj) and not obj.is_valid:
            btns.append(self.create_custom_button('validate', pk, classnames_add, classnames_exclude))

        if 'reconcile' not in exclude and user_can_reconcile and obj.is_valid and not obj.is_reconciled:
            btns.append(self.create_custom_button('reconcile', pk, classnames_add, classnames_exclude))

        if 'add_all_product' not in exclude and user_can_reconcile and not obj.is_valid and not obj.is_reconciled:
            btns.append(self.create_custom_button('add_all_product', pk, classnames_add, classnames_exclude))

        return btns
