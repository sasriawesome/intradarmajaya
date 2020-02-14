from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin.views import CreateView, IndexView, InspectView
from wagtail.contrib.modeladmin.helpers import PermissionHelper, ButtonHelper
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, ObjectList, InlinePanel, TabbedInterface

from .models import Discussion, DiscussionCategory


class DiscussionIndexView(IndexView):
    def inspect_url(self):
        return self.url_helper.get_action_url('inspect')


class DiscussionInspectView(InspectView):
    meta_title = ''
    page_title = ''
    page_subtitle = 'Ini subtitle'

    def get_page_title(self):
        return self.page_title

    def get_meta_title(self):
        return self.instance.title


class DiscussionCreateView(CreateView):
    def get_instance(self):
        instance = super().get_instance()
        instance.creator = self.request.user
        return instance


class DiscussionButtonHelper(ButtonHelper):
    show_button_classnames = ['bicolor', 'icon', 'icon-view']
    inspect_button_classnames = ['view']

    def show_mine_button(self, classnames_show=None, classnames_exclude=None):
        if classnames_show is None:
            classnames_show = []
        if classnames_exclude is None:
            classnames_exclude = []
        classnames = self.show_button_classnames + classnames_show
        cn = self.finalise_classname(classnames, classnames_exclude)
        return {
            'url': self.url_helper.index_url + '?creator_id=%s' % self.request.user.id,
            'label': _('Show My %ss') % self.verbose_name,
            'classname': cn,
            'title': _('Show only my %ss ') % self.verbose_name,
        }


class DiscussionPermissionHelper(PermissionHelper):
    def user_can_edit_obj(self, user, obj):
        edit_own = self.get_perm_codename('change')
        edit_other = self.get_perm_codename('changeother')
        can_edit = self.user_has_specific_permission(user, edit_own)
        can_edit_other = self.user_has_specific_permission(user, edit_other)
        if can_edit_other:
            return can_edit_other
        else:
            return can_edit and obj.creator == user

    def user_can_delete_obj(self, user, obj):
        delete_own = self.get_perm_codename('change')
        delete_other = self.get_perm_codename('deleteother')
        can_delete = self.user_has_specific_permission(user, delete_own)
        can_delete_other = self.user_has_specific_permission(user, delete_other)
        if can_delete_other:
            return can_delete_other
        else:
            return can_delete and obj.creator == user


class DiscussionModelAdmin(ModelAdmin):
    menu_label = _('Discusses')
    menu_icon = 'fa-comments'
    model = Discussion
    inspect_view_enabled = True
    index_view_class = DiscussionIndexView
    create_view_class = DiscussionCreateView
    inspect_view_class = DiscussionInspectView
    list_per_page = 15
    search_fields = ['title', 'creator__first_name']
    list_filter = ['date_created', 'category']
    list_display = ['title', 'date_created', 'creator']
    permission_helper_class = DiscussionPermissionHelper
    button_helper_class = DiscussionButtonHelper

    edit_handler = TabbedInterface([
        ObjectList([
            FieldPanel('title'),
            FieldPanel('summary'),
            MultiFieldPanel([
                FieldPanel('category'),
                FieldPanel('tags'),
            ], heading='Grouping'),
            FieldPanel('body'),
        ], heading=_('Content')),
        ObjectList([
            InlinePanel('gallery_images', label="Gallery images"),
        ], heading=_('Gallery')),
        ObjectList([
            FieldPanel('show_comment'),
            FieldPanel('status'),
        ], heading=_('Options'))
    ])

    def get_queryset(self, request):
        user = request.user
        qs = super().get_queryset(request)
        if user.is_superuser:
            return qs
        elif self.permission_helper.user_has_specific_permission(user, 'changeother'):
            return qs
        else:
            owner_filter = (
                models.Q(status__exact=self.model.PUBLISHED)
                | models.Q(creator__exact=request.user)
            )
            return qs.filter(owner_filter)


class DiscussionCategoryModelAdmin(ModelAdmin):
    menu_icon = 'fa-tags'
    menu_label = _('Categories')
    model = DiscussionCategory

    edit_handler = ObjectList([
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('description')
        ])
    ])