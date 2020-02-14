from django import forms

from django_select2.forms import Select2MultipleWidget

from wagtailkit.employees.models import Chairman
from wagtailkit.ememo.models import Memo

class MemoForm(forms.ModelForm):
    class Media:
        js = (
            'admin/js/vendor/jquery/jquery.min.js',
            'admin/js/vendor/select2/select2.full.min.js',
        )
        css = {
            'all': (
                'admin/css/vendor/select2/select2.min.css',
            )
        }

    class Meta:
        model = Memo
        exclude = ('date_created',)

    receiver = forms.ModelMultipleChoiceField(
        queryset=Chairman.objects.all(),
        widget=Select2MultipleWidget())
    cc = forms.ModelMultipleChoiceField(
        queryset=Chairman.objects.all(),
        widget=Select2MultipleWidget())