from wagtail.contrib.modeladmin.helpers import AdminURLHelper, PermissionHelper


class ImportExportAdminURLHelperMixin(AdminURLHelper):

    def get_imex_url_pattern(self, action):
        if action in ('export', 'import', 'process_import'):
            return self._get_action_url_pattern(action)
        return self._get_object_specific_action_url_pattern(action)

    def export_url(self):
        return self.get_action_url('export')

    def import_url(self):
        return self.get_action_url('import')


class ImportExportPermissionHelperMixin(PermissionHelper):

    def user_can_export(self, user):
        perm_codename = self.get_perm_codename('export')
        return self.user_has_specific_permission(user, perm_codename)

    def user_can_import(self, user):
        perm_codename = self.get_perm_codename('import')
        return self.user_has_specific_permission(user, perm_codename)