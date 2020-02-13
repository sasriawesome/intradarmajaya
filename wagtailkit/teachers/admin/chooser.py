from django.shortcuts import reverse
from django.conf.urls import url
from django.utils.translation import gettext_lazy as _
from wagtail.core import hooks

from generic_chooser.views import ModelChooserViewSet, ChooserListingTabMixin
from generic_chooser.widgets import AdminChooser

from wagtailkit.teachers.models import Teacher


class TeacherListingTab(ChooserListingTabMixin):
    listing_tab_template = 'modeladmin/academic/choosers/_listing_tab.html'
    results_template = 'modeladmin/teachers/choosers/results_teacher.html'

    def get_row_data(self, item):
        return {
            'choose_url': self.get_chosen_url(item),
            'title': self.get_object_string(item.name),
            'tid': item.tid,
            'rmu': item.rmu.name,
            'is_active': item.is_active
        }


class TeacherChooserViewSet(ModelChooserViewSet):
    icon = 'user'
    per_page = 5
    order_by = 'rmu'
    model = Teacher
    page_title = _('Teacher')
    fields = ['employee', 'tid', 'is_nidn', 'rmu', 'is_active']
    listing_tab_mixin_class = TeacherListingTab

    def get_urlpatterns(self):
        return [
            url(r'^$', self.choose_view, name='choose'),
            url(r'^(?P<pk>[-\w]+)/$', self.chosen_view, name='chosen'),
        ]


class TeacherChooser(AdminChooser):
    icon = 'user'
    input_type = 'hidden'
    model = Teacher
    choose_one_text = _("Choose a Teacher")
    choose_another_text = _("Choose another Teacher")
    clear_choice_text = _("Clear choice")
    link_to_chosen_text = _("Edit this teacher")
    choose_modal_url_name = 'teacher_chooser:choose'
    classname = 'teacher_chooser'


@hooks.register('register_admin_viewset')
def register_teacher_chooser_viewset():
    return TeacherChooserViewSet('teacher_chooser')
