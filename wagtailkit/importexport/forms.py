import os
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ImportExportSetting


class ImportForm(forms.Form):
    _settings = None
    request = None
    import_file = forms.FileField(
        label=_('File to import')
    )
    input_format = forms.ChoiceField(
        label=_('Format'),
        choices=(),
    )

    def __init__(self, formats, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = []
        self.request = request
        self._settings = ImportExportSetting.for_site(request.site)
        if self._settings:
            if self._settings.import_csv:
                choices.append((0, 'CSV',))
            if self._settings.import_xls:
                choices.append((1, 'XLS',))
            if self._settings.import_xlsx:
                choices.append((2, 'XLSX',))
            if self._settings.import_json:
                choices.append((5, 'JSON',))
        else:
            for i, f in enumerate(formats):
                choices.append((str(i), f().get_title(),))
            if len(formats) > 1:
                choices.insert(0, ('', '---'))
        self.fields['input_format'].choices = choices


class ConfirmImportForm(forms.Form):
    import_file_name = forms.CharField(widget=forms.HiddenInput())
    original_file_name = forms.CharField(widget=forms.HiddenInput())
    input_format = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_import_file_name(self):
        data = self.cleaned_data['import_file_name']
        data = os.path.basename(data)
        return data


class ExportForm(forms.Form):
    _settings = None
    request = None
    file_format = forms.ChoiceField(
        label=_('Format'),
        choices=(),
    )

    def __init__(self, formats, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = []
        self.request = request
        self._settings = ImportExportSetting.for_site(request.site)
        if self._settings:
            if self._settings.import_csv:
                choices.append((0, 'CSV',))
            if self._settings.import_xls:
                choices.append((1, 'XLS',))
            if self._settings.import_xlsx:
                choices.append((2, 'XLSX',))
            if self._settings.import_json:
                choices.append((5, 'JSON',))
        else:
            for i, f in enumerate(formats):
                choices.append((str(i), f().get_title(),))
            if len(formats) > 1:
                choices.insert(0, ('', '---'))
            self.fields['input_format'].choices = choices

        self.fields['file_format'].choices = choices
