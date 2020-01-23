from django.contrib import admin
from django.conf.urls import url

from wagtail.contrib.modeladmin.options import ModelAdmin

from .views import DetailPDFView, IndexPDFView
from .helpers import PrintPDFButtonHelperMixin, PrintPDFAdminURLHelperMixin


class PrintPDFModelAdminMixin(ModelAdmin):
    pdf_list_display = None

    index_print_enabled = False
    index_document_title = None
    index_pdf_filename = None
    index_pdf_template = None
    index_print_view_class = IndexPDFView

    detail_document_title = None
    detail_pdf_filename = None
    detail_pdf_template = None
    detail_print_view_class = DetailPDFView

    url_helper_class = PrintPDFAdminURLHelperMixin
    button_helper_class = PrintPDFButtonHelperMixin


    def get_admin_urls_for_registration(self):
        urls = super().get_admin_urls_for_registration()
        extra_urls = (
            url(self.url_helper.get_action_url_pattern('print_detail'),
                self.detail_print_view,
                name=self.url_helper.get_action_url_name('print_detail')),
        )

        if self.index_print_enabled:
            extra_urls += (
                url(self.url_helper.get_action_url_pattern('print_index'),
                    self.index_print_view,
                    name=self.url_helper.get_action_url_name('print_index')),
            )
        return extra_urls + urls

    def index_print_view(self, request):
        kwargs = {'model_admin': self}
        view_class = self.index_print_view_class
        return view_class.as_view(**kwargs)(request)

    def detail_print_view(self, request, instance_pk):
        kwargs = {'model_admin': self, 'instance_pk': instance_pk}
        view_class = self.detail_print_view_class
        return view_class.as_view(**kwargs)(request)
