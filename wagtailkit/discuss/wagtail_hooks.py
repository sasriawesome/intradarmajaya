from wagtail.admin.navigation import get_site_for_user
from wagtail.admin.site_summary import SummaryItem
from wagtail.core import hooks

from .models import Discussion


class DiscussionWelcomePanel(SummaryItem):
    order = 50
    template = 'modeladmin/discuss/admin_homepage_summary.html'

    def get_context(self):
        site_name = get_site_for_user(self.request.user)['site_name']
        return {
            'site_name': site_name,
            'first_discuss': Discussion.objects.filter(status=Discussion.PUBLISHED)[:1],
            'recent_discussions': Discussion.objects.filter(status=Discussion.PUBLISHED)[1:5],
        }

    def is_shown(self):
        # return permission_policy.user_has_any_permission(
        #     self.request.user, ['add', 'change', 'delete']
        # )
        return True


@hooks.register('construct_homepage_panels')
def add_discussion_welcome_panel(request, panels):
    panels.append(DiscussionWelcomePanel(request))
