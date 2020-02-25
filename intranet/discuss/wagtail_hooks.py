from django.contrib.auth import get_permission_codename
from wagtail.admin.navigation import get_site_for_user
from wagtail.admin.site_summary import SummaryItem
from wagtail.core import hooks

from wagtailkit.admin.helpers import PermissionHelper
from wagtailkit.discuss.models import Discussion

ph_discussion = PermissionHelper(Discussion)


class DiscussionWelcomePanel(SummaryItem):
    order = 1
    template = 'modeladmin/discuss/admin_homepage_summary.html'

    def get_context(self):
        site_name = get_site_for_user(self.request.user)['site_name']
        return {
            'site_name': site_name,
            'first_discuss': Discussion.objects.filter(status=Discussion.PUBLISHED)[:1],
            'recent_discussions': Discussion.objects.filter(status=Discussion.PUBLISHED)[1:5],
        }

    def is_shown(self):
        return ph_discussion.user_has_any_permissions(self.request.user)


@hooks.register('construct_homepage_panels')
def add_discussion_welcome_panel(request, panels):
    discussion_summary = DiscussionWelcomePanel(request)
    if discussion_summary.is_shown():
        panels.append(DiscussionWelcomePanel(request))