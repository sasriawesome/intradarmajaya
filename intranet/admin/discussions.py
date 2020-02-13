from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdminGroup
from wagtailkit.discuss.admin import DiscussionModelAdmin, DiscussionCategoryModelAdmin


class DiscussionsModelAdminGroup(ModelAdminGroup):
    menu_icon = 'fa-twitch'
    menu_label = _('Discussions')
    items = [
        DiscussionModelAdmin,
        DiscussionCategoryModelAdmin
    ]