from django import forms
from django.utils.translation import gettext_lazy as _
from wagtailkit.academic.models import SchoolYear, ProgramStudy
from wagtailkit.students.models import Student

class StudentRegistrationForm(forms.Form):

    fullname = forms.CharField()
    email = forms.EmailField()
    registration = forms.ChoiceField(
        choices=(('1','Reguler'), ('P', 'Transfer')),
        initial='1'
    )
    registration_id = forms.CharField()
    program_study = forms.ModelChoiceField(
        queryset=ProgramStudy.objects.all(),
        widget=forms.Select())
    year_of_force = forms.ModelChoiceField(
        queryset=SchoolYear.objects.all(),
        widget=forms.Select())
    are_you_sure = forms.BooleanField(
        help_text=_("Im sure, create this student!")
    )

