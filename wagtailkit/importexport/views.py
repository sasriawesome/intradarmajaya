from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property
from django.utils.encoding import force_text, force_str
from django.utils.module_loading import import_string
from django.utils.decorators import method_decorator
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from django.contrib.admin.utils import capfirst
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.conf import settings

from import_export.resources import modelresource_factory
from import_export.tmp_storages import TempFolderStorage
from import_export.formats.base_formats import DEFAULT_FORMATS
from import_export.signals import post_export, post_import
from import_export.results import RowResult

from wagtail.core.models import Page
from wagtail.admin.messages import messages
from wagtail.contrib.modeladmin.views import IndexView

from wagtailkit.importexport.forms import ImportForm, ExportForm, ConfirmImportForm

SKIP_ADMIN_LOG = getattr(settings, 'IMPORT_EXPORT_SKIP_ADMIN_LOG', False)
TMP_STORAGE_CLASS = getattr(settings, 'IMPORT_EXPORT_TMP_STORAGE_CLASS', TempFolderStorage)

if isinstance(TMP_STORAGE_CLASS, str):
    TMP_STORAGE_CLASS = import_string(TMP_STORAGE_CLASS)


class ImportExportIndexView(IndexView):
    """ Add import export buttons and permission to index page """

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = {
            'user_can_export': self.permission_helper.user_can_export(user),
            'user_can_import': self.permission_helper.user_can_import(user)
        }
        context.update(kwargs)
        return super().get_context_data(**context)


class ImexBaseView(TemplateView, FormView):
    """
    Groups together common functionality for all app views.
    """
    meta_title = ''
    page_title = ''
    page_subtitle = ''
    tmp_storage_class = TempFolderStorage
    formats = DEFAULT_FORMATS
    encoding = "utf-8"
    model = None
    model_admin = None
    skip_admin_log = None
    resource_class = None

    def __init__(self, model_admin, model=None, **kwargs):
        super().__init__(**kwargs)
        self.model = model or model_admin.model
        self.opts = self.model._meta
        self.app_label = force_str(self.opts.app_label)
        self.model_name = force_str(self.opts.model_name)
        self.verbose_name = force_str(self.opts.verbose_name)
        self.verbose_name_plural = force_str(self.opts.verbose_name_plural)
        self.pk_attname = self.opts.pk.attname
        self.model_admin = model_admin
        self.is_pagemodel = issubclass(self.model, Page)
        self.permission_helper = model_admin.permission_helper
        self.url_helper = model_admin.url_helper

    def check_action_permitted(self, user):
        return True

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not self.check_action_permitted(request.user):
            raise PermissionDenied
        button_helper_class = self.model_admin.get_button_helper_class()
        self.button_helper = button_helper_class(self, request)
        return super().dispatch(request, *args, **kwargs)

    @cached_property
    def menu_icon(self):
        return self.model_admin.get_menu_icon()

    @cached_property
    def header_icon(self):
        return self.menu_icon

    @cached_property
    def index_url(self):
        return self.url_helper.index_url

    @cached_property
    def create_url(self):
        return self.url_helper.create_url

    @cached_property
    def export_url(self):
        return self.url_helper.export_url

    @cached_property
    def import_url(self):
        return self.url_helper.import_url

    @cached_property
    def process_import_url(self):
        return self.url_helper.get_action_url('process_import')

    def get_page_title(self):
        return '%s %s' % (self.page_title, capfirst(self.opts.verbose_name_plural))

    def get_meta_title(self):
        return self.meta_title or self.get_page_title()

    def get_base_queryset(self, request=None):
        return self.model_admin.get_queryset(request or self.request)

    def get_context_data(self, **kwargs):
        context = {
            'view': self,
            'model_admin': self.model_admin,
        }
        context.update(kwargs)
        return super().get_context_data(**context)

    def get_skip_admin_log(self):
        if self.skip_admin_log is None:
            return SKIP_ADMIN_LOG
        else:
            return self.skip_admin_log

    def get_tmp_storage_class(self):
        if self.model_admin.tmp_storage_class:
            return self.model_admin.tmp_storage_class
        else:
            return self.tmp_storage_class

    def get_resource_class(self):
        """Returns ResourceClass """
        if self.model_admin.resource_class:
            return self.model_admin.resource_class
        elif self.resource_class:
            return self.resource_class
        else:
            return modelresource_factory(self.model)

    def get_resource(self, **kwargs):
        return self.get_resource_class()(**kwargs)

    def get_resource_kwargs(self, request, *args, **kwargs):
        return {}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs

class ImportBaseView(ImexBaseView):
    page_title = _('Import')
    import_template_name = 'modeladmin/importexport/import.html'

    def get_template_names(self):
        model_admin_template = getattr(self.model_admin, 'import_template_name', None)
        if model_admin_template:
            return model_admin_template.import_template_name
        else:
            return self.import_template_name

    def get_import_formats(self):
        return [f for f in self.formats if f().can_import()]

    def get_import_data_kwargs(self, request, *args, **kwargs):
        form = kwargs.get('form')
        if form:
            kwargs.pop('form')
            return kwargs
        return {}

    def get_context_data(self, **kwargs):
        res_kwargs = self.get_resource_kwargs(self.request, **kwargs)
        resource = self.get_resource(**res_kwargs)
        context = {
            'fields': [f.column_name for f in resource.get_user_visible_fields()],
        }
        context.update(**kwargs)
        return super().get_context_data(**context)

    def get_form(self, form_class=None):
        import_formats = self.get_import_formats()
        form_class = self.get_form_class()
        form = form_class(import_formats, **self.get_form_kwargs())
        return form


class ImportView(ImportBaseView):
    page_title = _('Import')
    form_class = ImportForm

    def write_to_tmp_storage(self, import_file, input_format):
        tmp_storage = self.get_tmp_storage_class()()
        data = bytes()
        for chunk in import_file.chunks():
            data += chunk

        tmp_storage.save(data, input_format.get_read_mode())
        return tmp_storage

    def form_valid(self, form, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        import_formats = self.get_import_formats()
        input_format = import_formats[
            int(form.cleaned_data['input_format'])
        ]()
        import_file = form.cleaned_data['import_file']
        # first always write the uploaded file to disk as it may be a
        # memory file or else based on settings upload handlers
        tmp_storage = self.write_to_tmp_storage(import_file, input_format)

        # then read the file, using the proper format-specific mode
        # warning, big files may exceed memory
        try:
            data = tmp_storage.read(input_format.get_read_mode())
            if not input_format.is_binary() and self.encoding:
                data = force_text(data, self.encoding)
            dataset = input_format.create_dataset(data)
        except UnicodeDecodeError as e:
            msg = _("Imported file has a wrong encoding: %s" % e)
            messages.add_message(self.request, level=messages.ERROR, message=msg)
            return self.render_to_response(context)
        except Exception as e:
            msg = _("%s encountered while trying to read file: %s" % (type(e).__name__, import_file.name))
            messages.add_message(self.request, level=messages.ERROR, message=msg)
            return self.render_to_response(context)

        # prepare kwargs for import data, if needed
        res_kwargs = self.get_resource_kwargs(self.request, form=form, *args, **kwargs)
        resource = self.get_resource(**res_kwargs)

        # prepare additional kwargs for import_data, if needed
        imp_kwargs = self.get_import_data_kwargs(self.request, form=form, *args, **kwargs)
        result = resource.import_data(
            dataset,
            dry_run=True,
            raise_errors=False,
            file_name=import_file.name,
            user=self.request.user,
            **imp_kwargs
        )

        context['result'] = result

        if not result.has_errors() and not result.has_validation_errors():
            initial = {
                'import_file_name': tmp_storage.name,
                'original_file_name': import_file.name,
                'input_format': form.cleaned_data['input_format'],
            }
            confirm_form = ConfirmImportForm
            kwargs = self.get_form_kwargs()
            kwargs['data'] = initial
            context['confirm_form'] = confirm_form(**kwargs)

        return self.render_to_response(context)

    def form_invalid(self, form, *args, **kwargs):
        context = {
            **self.get_context_data(**kwargs),
            'form': form,
        }
        context.update(**context)
        return self.render_to_response(context)


class ProcessImportView(ImportBaseView):
    form_class = ConfirmImportForm

    def get_success_message(self, result):
        opts = self.opts
        msg = _('Import finished, with {} new and ' '{} updated {}.')
        success_message = msg.format(
            result.totals[RowResult.IMPORT_TYPE_NEW],
            result.totals[RowResult.IMPORT_TYPE_UPDATE],
            opts.verbose_name_plural
        )
        return success_message

    def get_form(self, form_class=None):
        form_class = self.get_form_class()
        form = form_class(**self.get_form_kwargs())
        return form

    def get_error_message(self):
        model_name = self.verbose_name
        return _("The %s could not be imported due to errors.") % model_name

    def get_success_url(self):
        return self.url_helper.index_url

    def form_invalid(self, form):
        messages.add_message(self.request, level=messages.ERROR, message=self.get_error_message())
        return redirect(self.url_helper.import_url())

    def form_valid(self, confirm_form):
        import_formats = self.get_import_formats()
        input_format = import_formats[
            int(confirm_form.cleaned_data['input_format'])
        ]()
        tmp_storage = self.get_tmp_storage_class()(
            name=confirm_form.cleaned_data['import_file_name']
        )
        data = tmp_storage.read(input_format.get_read_mode())
        if not input_format.is_binary() and self.encoding:
            data = force_text(data, self.encoding)

        dataset = input_format.create_dataset(data)
        result = self.process_dataset(dataset, confirm_form, **self.get_form_kwargs())
        tmp_storage.remove()

        self.generate_log_entries(result, self.request)
        post_import.send(sender=None, model=self.model)

        messages.add_message(
            self.request,
            level=messages.SUCCESS,
            message=self.get_success_message(result))
        return redirect(self.get_success_url())

    def process_dataset(self, dataset, confirm_form, request, *args, **kwargs):

        res_kwargs = self.get_resource_kwargs(request, *args, **kwargs)
        resource = self.get_resource(**res_kwargs)

        imp_kwargs = self.get_import_data_kwargs(request, *args, **kwargs)
        return resource.import_data(
            dataset, dry_run=False, raise_errors=True,
            file_name=confirm_form.cleaned_data['original_file_name'],
            user=request.user, **imp_kwargs)

    def generate_log_entries(self, result, request):
        if not self.get_skip_admin_log():
            # Add imported objects to LogEntry
            logentry_map = {
                RowResult.IMPORT_TYPE_NEW: ADDITION,
                RowResult.IMPORT_TYPE_UPDATE: CHANGE,
                RowResult.IMPORT_TYPE_DELETE: DELETION,
            }
            content_type_id = ContentType.objects.get_for_model(self.model).pk
            for row in result:
                if row.import_type != row.IMPORT_TYPE_ERROR and row.import_type != row.IMPORT_TYPE_SKIP:
                    LogEntry.objects.log_action(
                        user_id=request.user.pk,
                        content_type_id=content_type_id,
                        object_id=row.object_id,
                        object_repr=row.object_repr,
                        action_flag=logentry_map[row.import_type],
                        change_message=_("%s through import_export" % row.import_type),
                    )


class ImportInlineView(ImportView):
    form_class = ImportForm
    parent_model = None
    model = None  # Inline Model
    resource_class = None  # Resource for Inline Model
    instance = None
    instance_pk = None

    def __init__(self, model_admin, instance_pk, model=None, **kwargs):
        super().__init__(model_admin, model, **kwargs)
        self.parent_model = self.model_admin.model
        self.parent_opts = self.parent_model._meta
        self.instance_pk = instance_pk
        self.instance = get_object_or_404(self.parent_model, pk=instance_pk)

    @cached_property
    def process_import_url(self):
        return self.url_helper.get_action_url('process_import_inline', self.instance_pk)

    def get_resource_class(self):
        return self.resource_class or self.model_admin.inline_resource_class

    def get_page_title(self):
        return '%s %s for %s' % (
            self.page_title,
            capfirst(self.opts.verbose_name_plural),
            capfirst(self.parent_opts.verbose_name))

    def get_context_data(self, **kwargs):
        res_kwargs = self.get_resource_kwargs(self.request, **kwargs)
        resource = self.get_resource(**res_kwargs)
        context = {
            'fields': [f.column_name for f in resource.get_user_visible_fields()],
        }
        context.update(**kwargs)
        return super().get_context_data(**context)

    def get_resource(self, **kwargs):
        return super().get_resource(parent=self.instance, **kwargs)


class ProcessImporInlinetView(ProcessImportView):

    def __init__(self, model_admin, instance_pk, model=None, **kwargs):
        super().__init__(model_admin, model, **kwargs)
        self.parent_model = self.model_admin.model
        self.parent_opts = self.parent_model._meta
        self.instance_pk = instance_pk
        self.instance = get_object_or_404(self.parent_model, pk=instance_pk)


class ExportView(ImexBaseView):
    page_title = _('Export')
    form_class = ExportForm
    export_template_name = 'modeladmin/importexport/export.html'

    def get_template_names(self):
        model_admin_template = getattr(self.model_admin, 'export_template_name', None)
        if model_admin_template:
            return model_admin_template.export_template_name
        else:
            return self.export_template_name

    def get_export_formats(self):
        formats = [f for f in self.formats if f().can_export()]
        return formats

    def get_export_filename(self, request, queryset, file_format):
        date_str = timezone.now().strftime('%Y-%m-%d')
        filename = "%s-%s.%s" % (self.model.__name__, date_str, file_format.get_extension())
        return filename

    def get_export_queryset(self, request):
        return self.get_base_queryset(request)

    def get_export_data(self, file_format, queryset, *args, **kwargs):
        """
        Returns file_format representation for given queryset.
        """
        request = kwargs.pop("request")
        if not self.permission_helper.user_can_export(request.user):
            raise PermissionDenied

        res_kwargs = self.get_resource_kwargs(request)
        data = self.get_resource(**res_kwargs).export(queryset, *args, **kwargs)
        export_data = file_format.export_data(data)
        return export_data

    def get_form(self, form_class=None):
        formats = self.get_export_formats()
        form_class = self.get_form_class()
        form = form_class(formats, **self.get_form_kwargs())
        return form

    def form_valid(self, form, *args, **kwargs):
        formats = self.get_export_formats()
        file_format = formats[
            int(form.cleaned_data['file_format'])
        ]()
        queryset = self.get_export_queryset(self.request)
        export_data = self.get_export_data(file_format, queryset, request=self.request)

        content_type = file_format.get_content_type()
        response = HttpResponse(export_data, content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename="%s"' % (
            self.get_export_filename(self.request, queryset, file_format),
        )
        post_export.send(sender=None, model=self.model)
        return response

    def form_invalid(self, form, *args, **kwargs):
        context = {
            **self.get_context_data(),
            'form': form
        }
        return self.render_to_response(context)
