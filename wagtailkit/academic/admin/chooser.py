from django.shortcuts import reverse
from django.conf.urls import url
from django.utils.translation import gettext_lazy as _
from wagtail.core import hooks

from generic_chooser.views import ModelChooserViewSet, ChooserListingTabMixin, ModelChooserMixin
from generic_chooser.widgets import AdminChooser

from wagtailkit.academic.models import ResourceManagementUnit, ProgramStudy, Course


class RMUListingTab(ChooserListingTabMixin):
    listing_tab_template = 'modeladmin/academic/choosers/_listing_tab.html'
    results_template = 'modeladmin/academic/choosers/results_rmu.html'

    def get_row_data(self, item):
        return {
            'choose_url': self.get_chosen_url(item),
            'title': self.get_object_string(item),
            'code': item.code,
            'number': item.number,
            'parent': item.parent,
        }


class RMUChooserViewSet(ModelChooserViewSet):
    icon = 'user'
    per_page = 5
    order_by = 'name'
    model = ResourceManagementUnit
    page_title = _('Resource Management Unit')
    fields = ['parent', 'name', 'status', 'code', 'number']
    listing_tab_mixin_class = RMUListingTab

    def get_urlpatterns(self):
        return [
            url(r'^$', self.choose_view, name='choose'),
            url(r'^(?P<pk>[-\w]+)/$', self.chosen_view, name='chosen'),
        ]


class RMUChooser(AdminChooser):
    show_edit_link = True
    input_type = 'hidden'
    choose_one_text = _("Choose an RMU")
    choose_another_text = _("Choose another RMU")
    clear_choice_text = _("Clear choice")
    link_to_chosen_text = _("Edit this RMU")
    model = ResourceManagementUnit
    choose_modal_url_name = 'rmu_chooser:choose'
    classname = 'custom_chooser rmu_chooser'


@hooks.register('register_admin_viewset')
def register_rmu_chooser_viewset():
    return RMUChooserViewSet('rmu_chooser')


class CourseListingTab(ChooserListingTabMixin):
    listing_tab_template = 'modeladmin/academic/choosers/_listing_tab.html'
    results_template = 'modeladmin/academic/choosers/results_course.html'

    def get_row_data(self, item):
        return {
            'choose_url': self.get_chosen_url(item),
            'title': self.get_object_string(item.name),
            'inner_id': item.inner_id,
            'rmu': item.rmu.name,
            'year_offered': item.year_offered,
            'level': item.level,
        }


class CourseChooserViewSet(ModelChooserViewSet):
    icon = 'user'
    per_page = 5
    order_by = 'rmu'
    model = Course
    page_title = _('Course')
    fields = ['name', 'rmu', 'course_type', 'course_group', 'level', 'year_offered']
    listing_tab_mixin_class = CourseListingTab

    def get_urlpatterns(self):
        return [
            url(r'^$', self.choose_view, name='choose'),
            url(r'^(?P<pk>[-\w]+)/$', self.chosen_view, name='chosen'),
        ]

class CourseChooser(AdminChooser):
    input_type = 'hidden'
    model = Course
    choose_one_text = _("Choose a Course")
    choose_another_text = _("Choose another Course")
    clear_choice_text = _("Clear choice")
    link_to_chosen_text = _("Edit this Course")
    choose_modal_url_name = 'course_chooser:choose'
    classname = 'custom_chooser course_chooser'


@hooks.register('register_admin_viewset')
def register_course_chooser_viewset():
    return CourseChooserViewSet('course_chooser')