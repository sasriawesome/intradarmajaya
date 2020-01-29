from django import forms

from .models import LabService

class LabServiceForm(forms.ModelForm):
    class Meta:
        model = LabService
        fields = (
            'name',
            'service_type',
            'category',
            'description',
            'unit_price',
            'unit_of_measure',
            'is_active'
        )