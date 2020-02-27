from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdminGroup, modeladmin_register
from wagtailkit.discuss.admin import DiscussionModelAdmin, DiscussionCategoryModelAdmin


class DiscussionsModelAdminGroup(ModelAdminGroup):
    menu_icon = 'fa-twitch'
    menu_label = _('Discussions')
    items = [
        DiscussionModelAdmin,
        DiscussionCategoryModelAdmin
    ]

modeladmin_register(DiscussionsModelAdminGroup)