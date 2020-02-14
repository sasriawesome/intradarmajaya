from django.utils import timezone
from django.shortcuts import get_object_or_404

from wkhtmltopdf.views import PDFTemplateView
from .models import PrintPDFSetting


class ModelPDFBaseView(PDFTemplateView):
    title = None
    model_admin = None
    show_content_in_browser = True
    template_name = None
    cover_template = 'modeladmin/pdf/cover.html'
    header_template = 'modeladmin/pdf/header.html'
    footer_template = 'modeladmin/pdf/footer.html'

    cmd_options = {
        'margin-top': 40,
        'margin-left': 25,
        'margin-right': 25,
        'margin-bottom': 25,
    }

    def __init__(self, model_admin, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_admin = model_admin
        self.model = model_admin.model
        self.opts = self.model._meta

    def get(self, request, *args, **kwargs):
        self.apply_settings(request)
        return super().get(request, *args, **kwargs)

    def get_settings(self, request):
        return PrintPDFSetting.for_site(request.site)

    def apply_settings(self, request):
        pass

    def get_title(self):
        return self.title or self.opts.verbose_name

    def get_context_data(self, **kwargs):
        context = {
            'title': self.get_title(),
            'opts': self.opts,
        }
        context.update(**kwargs)
        return super().get_context_data(**context)

    def get_filename(self):
        if not self.filename:
            self.filename = '%s_%s_%s' % (
                self.opts.app_label,
                self.opts.model_name, timezone.now().strftime('%d%m%Y')
            )
        return

    def get_cmd_options(self):
        return self.cmd_options


class IndexPDFView(ModelPDFBaseView):
    def __init__(self, model_admin, *args, **kwargs):
        super().__init__(model_admin, *args, **kwargs)
        self.model_admin = model_admin
        self.model = model_admin.model
        self.opts = self.model._meta

    def apply_settings(self, request):
        settings = self.get_settings(request)
        self.cmd_options = {
            'margin-top': settings.index_margin_top or 40,
            'margin-left': settings.index_margin_left or 25,
            'margin-right': settings.index_margin_right or 25,
            'margin-bottom': settings.index_margin_bottom or 25,
            'orientation': settings.index_orientation or 'landscape'
        }
        if settings.index_show_cover:
            self.cover_template = None
        if settings.index_show_header:
            self.header_template = None
        if settings.index_show_footer:
            self.footer_template = None

    def get_title(self):
        return self.model_admin.index_document_title or super().get_title()

    def get_filename(self):
        if getattr(self.model_admin, 'index_pdf_filename', None):
            self.filename = self.model_admin.index_pdf_filename
        elif not self.filename:
            self.filename = '%s_%s_index_%s' % (
                self.opts.app_label,
                self.opts.model_name, timezone.now().strftime('%d%m%Y')
            )
        return

    def get_list_display(self):
        return getattr(self.model_admin, 'pdf_list_display', None)

    def get_results(self, request):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = {
            'headers': self.get_list_display(),
            'results': self.get_results(self.request),
            'is_print': True
        }
        context.update(**kwargs)
        return super().get_context_data(**context)

    def get_template_names(self):
        app_label = self.opts.app_label.lower()
        model_name = self.opts.model_name.lower()
        index_pdf_template = getattr(self.model_admin, 'index_pdf_template')
        if index_pdf_template:
            return index_pdf_template
        else:
            return [
                'modeladmin/%s/%s/print_index.html' % (app_label, model_name),
                'modeladmin/%s/print_index.html' % (app_label),
                'modeladmin/print_index.html',
            ]


class DetailPDFView(ModelPDFBaseView):
    instance = None
    instance_pk = None

    def __init__(self, model_admin, instance_pk, *args, **kwargs):
        super().__init__(model_admin, *args, **kwargs)
        self.instance_pk = instance_pk
        self.instance = get_object_or_404(self.model, pk=instance_pk)

    def get_title(self):
        return self.model_admin.detail_document_title or super().get_title()

    def apply_settings(self, request):
        settings = self.get_settings(request)
        self.cmd_options = {
            'margin-top': settings.detail_margin_top or 40,
            'margin-left': settings.detail_margin_left or 25,
            'margin-right': settings.detail_margin_right or 25,
            'margin-bottom': settings.detail_margin_bottom or 25,
            'orientation': settings.detail_orientation or 'portrait'
        }
        if not settings.detail_show_cover:
            self.cover_template = None
        if not settings.detail_show_header:
            self.header_template = None
        if not settings.detail_show_footer:
            self.footer_template = None

    def get_filename(self):
        if getattr(self.model_admin, 'detail_pdf_filename', None):
            return self.model_admin.detail_pdf_filename
        elif not self.filename:
            self.filename = '%s_%s_index_%s' % (
                self.opts.app_label,
                self.opts.model_name, timezone.now().strftime('%d%m%Y')
            )
        return

    def get_context_data(self, **kwargs):
        context = {'instance': self.instance, 'is_print': True}
        context.update(**kwargs)
        return super().get_context_data(**context)

    def get_template_names(self):
        app_label = self.opts.app_label.lower()
        model_name = self.opts.model_name.lower()
        detail_pdf_template = getattr(self.model_admin, 'detail_pdf_template', None)
        if detail_pdf_template:
            return detail_pdf_template
        else:
            return [
                'modeladmin/%s/%s/print_detail.html' % (app_label, model_name),
                'modeladmin/%s/print_detail.html' % (app_label),
                'modeladmin/print_detail.html',
            ]
