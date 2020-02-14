from django.shortcuts import render
from django.conf.urls import url

from wagtail.contrib.modeladmin.options import ModelAdmin
from wagtail.admin.edit_handlers import EditHandler, FieldPanel, MultiFieldPanel, ObjectList

from .views import ImportExportIndexView, ExportView, ImportView, ProcessImportView, ImportInlineView
from .helpers import ImportExportAdminURLHelperMixin, ImportExportPermissionHelperMixin


class ImportExportModelAdminMixin(ModelAdmin):
    export_enabled = True
    import_enabled = True
    import_inline_enabled = False

    resource_class = None
    imex_setting_class = None
    tmp_storage_class = None  # storage class for saving temporary files

    url_helper_class = ImportExportAdminURLHelperMixin
    permission_helper_class = ImportExportPermissionHelperMixin
    index_view_class = ImportExportIndexView
    export_view_class = ExportView
    import_view_class = ImportView
    process_import_view_class = ProcessImportView

    inline_model = None
    inline_resource_class = None
    inline_import_view_class = ImportInlineView

    index_template_name = 'modeladmin/importexport/index.html'

    export_edit_handler = ObjectList([
        EditHandler('format')
    ])

    def get_admin_urls_for_registration(self):
        urls = super().get_admin_urls_for_registration()
        extra_urls = tuple()

        if self.export_enabled:
            extra_urls += (
                url(self.url_helper.get_imex_url_pattern('export'), self.export_view,
                    name=self.url_helper.get_action_url_name('export')),
            )

        if self.import_enabled:
            extra_urls += (
                url(self.url_helper.get_imex_url_pattern('import'), self.import_view,
                    name=self.url_helper.get_action_url_name('import')),
                url(self.url_helper.get_imex_url_pattern('process_import'), self.process_import_view,
                    name=self.url_helper.get_action_url_name('process_import')),
            )

        if self.import_inline_enabled:
            extra_urls += (
                url(self.url_helper.get_imex_url_pattern('import_inline'), self.import_inline_view,
                    name=self.url_helper.get_action_url_name('import_inline')),
                url(self.url_helper.get_imex_url_pattern('process_import_inline'), self.process_import_inline_view,
                    name=self.url_helper.get_action_url_name('process_import_inline')),
            )
        return extra_urls + urls

    def export_view(self, request):
        kwargs = {'model_admin': self}
        view_class = self.export_view_class
        return view_class.as_view(**kwargs)(request)

    def import_view(self, request):
        kwargs = {'model_admin': self}
        view_class = self.import_view_class
        return view_class.as_view(**kwargs)(request)

    def process_import_view(self, request):
        kwargs = {'model_admin': self}
        view_class = self.process_import_view_class
        return view_class.as_view(**kwargs)(request)

    def import_inline_view(self, request, instance_pk):
        kwargs = {'model_admin': self, 'instance_pk':instance_pk, 'model': self.inline_model}
        view_class = self.inline_import_view_class
        return view_class.as_view(**kwargs)(request, instance_pk)

    def process_import_inline_view(self, request, instance_pk):
        kwargs = {'model_admin': self, 'instance_pk': instance_pk, 'model': self.inline_model}
        view_class = self.process_import_view_class
        return view_class.as_view(**kwargs)(request)