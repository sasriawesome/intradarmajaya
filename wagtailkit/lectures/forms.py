from django import forms
from django.utils.translation import gettext_lazy as _
from django_select2 import forms as select2

from wagtailkit.academic.models import CurriculumCourse, Curriculum, AcademicYear, ResourceManagementUnit
from wagtailkit.teachers.models import Teacher
from wagtailkit.rooms.models import Room
from .models import Lecture


class LectureForm(forms.ModelForm):
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
        model = Lecture
        fields = [
            'code', 'name', 'academic_year', 'rmu', 'course',
            'teacher', 'assistant', 'room', 'date_start',
            'default_time_start', 'duration', 'series', 'status',
        ]

    code = forms.CharField()
    academic_year = forms.ModelChoiceField(
        queryset=AcademicYear.objects.all(),
        widget= select2.ModelSelect2Widget(
            model=AcademicYear,
            search_fields=['code__icontains']
        ))
    rmu = forms.ModelChoiceField(
        label=_('Program Study'),
        queryset=ResourceManagementUnit.objects.filter(status='4'),
        widget=select2.ModelSelect2Widget(
            model=ResourceManagementUnit,
            search_fields=['name__icontains']
        ))
    course = forms.ModelChoiceField(
        queryset=CurriculumCourse.objects.all(),
        widget=select2.ModelSelect2Widget(
            model=CurriculumCourse,
            search_fields=['course__name__icontains'],
            dependent_fields={
                'rmu': 'curriculum__rmu',
                'academic_year__semester': 'semester_type'
            },
            max_results=500,
        ))
    teacher = forms.ModelChoiceField(
        queryset=Teacher.objects.all(),
        widget=select2.ModelSelect2Widget(
            model=Teacher,
            search_fields=['employee__person__fullname__icontains']
        ))
    assistant = forms.ModelChoiceField(
        queryset=Teacher.objects.all(),
        widget=select2.ModelSelect2Widget(
            model=Teacher,
            search_fields=['employee__person__fullname__icontains']
        ))
    room = forms.ModelChoiceField(
        queryset=Room.objects.all(),
        widget=select2.ModelSelect2Widget(
            model=Room,
            search_fields=['employee__person__fullname__icontains']
        ))
    date_start = forms.DateField()
    default_time_start = forms.TimeField()
    duration = forms.IntegerField()
    series = forms.IntegerField()
    status = forms.ChoiceField(choices=Lecture.STATUS, initial=Lecture.PENDING)