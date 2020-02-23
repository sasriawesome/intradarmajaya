from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect, reverse
from django.conf.urls import url

from wagtailkit.autocompletes.edit_handlers import AutocompletePanel
from wagtail.admin.menu import MenuItem
from wagtail.admin.edit_handlers import ObjectList, FieldPanel, MultiFieldPanel, FieldRowPanel
from wagtail.contrib.modeladmin.views import WMABaseView, FormView
from wagtail.contrib.modeladmin.helpers import AdminURLHelper

from wagtailkit.admin.admin import ModelAdmin
from wagtailkit.persons.admin.admin_wagtail import PersonModelAdmin
from wagtailkit.persons.models import Person
from wagtailkit.students.models import Student, StudentPersonal, StudentScore, ConversionScore
from wagtailkit.students.forms import StudentRegistrationForm
from wagtailkit.academic.admin.admin_wagtail import ProgramStudyFilter


class StudentPersonalModelAdmin(PersonModelAdmin):
    model = StudentPersonal
    menu_icon = 'fa-user'
    menu_label = _('Student Personal')
    list_filter = ['date_created', 'is_matriculant']
    list_display = [
        'inner_id',
        'fullname_with_title',
        'gender',
        'is_matriculant',
        'is_student',
        'date_created']

    def is_student(self, obj):
        return obj.is_student

    is_student.boolean = True


class StudentAdminURLHelper(AdminURLHelper):
    def get_action_url_pattern(self, action):
        if action in ('create', 'register_student', 'choose_parent', 'index'):
            return self._get_action_url_pattern(action)
        return self._get_object_specific_action_url_pattern(action)


class RegisterStudentMenuItem(MenuItem):
    def is_shown(self, request):
        if request.user.has_perm('students.register_student') or request.user.is_superuser:
            return True
        else:
            return False


class RegisterStudentAdminView(WMABaseView, FormView):
    form_class = StudentRegistrationForm
    template_name = 'modeladmin/students/registration.html'
    page_title = _('Student Registration')
    instance = None

    def check_action_permitted(self, user):
        return self.permission_helper.user_has_specific_permission(user, 'register_student')

    def get_success_url(self):
        url_helper = self.model_admin.url_helper
        return reverse(url_helper.get_action_url_name('index'))

    def form_valid(self, form):
        data = form.cleaned_data
        with transaction.atomic():
            person = Person.objects.create(fullname=data.get('fullname'))
            student = Student(
                person=person,
                rmu=data.get('program_study'),
                year_of_force=data.get('year_of_force'),
                registration_id=data.get('registration_id'),
                registration=data.get('registration'),
                status=Student.ACTIVE)
            student.save()
            # Create User Account
            user_account = get_user_model().objects.create_user(
                username=student.sid,
                password=student.registration_id,
                email=data.get('email'), is_active=True)
            person.user_account = user_account
            # Set user group
            group, new_group = Group.objects.get_or_create(
                name='Mahasiswa',
                defaults={'name': 'Mahasiswa'})
            group.user_set.add(user_account)
            person.save()
        return redirect(self.get_success_url())


class StudentModelAdmin(ModelAdmin):
    model = Student
    url_helper_class = StudentAdminURLHelper
    register_student_view_class = RegisterStudentAdminView
    list_per_page = 25
    menu_icon = 'fa-user'
    search_fields = ['sid', 'person__fullname']
    list_filter = [ProgramStudyFilter, 'status', 'registration', 'year_of_force']
    list_display = ['sid', 'name', 'registration', 'status']

    edit_handler = ObjectList([
        MultiFieldPanel([
            AutocompletePanel('person'),
            AutocompletePanel('rmu'),
            AutocompletePanel('year_of_force'),
            FieldPanel('registration_id'),
            FieldPanel('registration'),
            FieldPanel('status'),
            FieldPanel('status_note'),
        ])
    ], heading=_('Student'))

    def get_admin_urls_for_registration(self):
        urls = super().get_admin_urls_for_registration()
        my_urls = (
            url(self.url_helper.get_action_url_pattern('register_student'),
                self.register_student_view, name='modeladmin_register_student'),
        )

        return urls + my_urls

    def register_student_view(self, request):
        kwargs = {'model_admin': self}
        view_class = self.register_student_view_class
        return view_class.as_view(**kwargs)(request)


class StudentScoreModelAdmin(ModelAdmin):
    search_fields = ['student__name', 'course__name']
    model = StudentScore
    menu_icon = 'fa-wpforms'
    list_filter = ['alphabetic', 'student__rmu', 'course__curriculum']
    list_per_page = 20
    list_display = ['sid', 'student', 'course_name', 'curriculum', 'num', 'alpha']

    edit_handler = ObjectList([
        MultiFieldPanel([
            AutocompletePanel('course'),
            AutocompletePanel('student'),
            FieldPanel('numeric'),
            FieldPanel('alphabetic'),
        ]),
    ])

    def sid(self, obj):
        return obj.sid

    def course_name(self, obj):
        return "{} {}".format(obj.cid, obj.course)

    def curriculum(self, obj):
        return obj.curriculum

    def num(self, obj):
        return obj.numeric

    def alpha(self, obj):
        return obj.alphabetic


class ConversionScoreModelAdmin(StudentScoreModelAdmin):
    search_fields = ['student__name', 'course__name']
    model = ConversionScore
    menu_icon = 'fa-wpforms'
    list_per_page = 20
    list_display = ['sid', 'student', 'course_name', 'curriculum', 'ori_name', 'num', 'alpha']
    edit_handler = ObjectList([
        MultiFieldPanel([
            AutocompletePanel('course'),
            AutocompletePanel('student'),
            FieldRowPanel([
                FieldPanel('numeric'),
                FieldPanel('alphabetic'),
            ])
        ]),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('ori_code'),
                FieldPanel('ori_name'),
            ]),
            FieldRowPanel([
                FieldPanel('ori_numeric_score'),
                FieldPanel('ori_alphabetic_score'),
            ]),
        ], heading=_('Original Scores'))
    ])
