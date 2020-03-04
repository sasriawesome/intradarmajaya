from django.db import transaction
from django.contrib.admin.utils import capfirst
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property

from wagtail.admin.messages import messages
from wagtail.contrib.modeladmin.views import ModelFormView, InstanceSpecificView
from wagtailkit.admin.views import InspectView


class StockCardInspectView(InspectView):
    def get_context_data(self, **kwargs):
        context = {
            'histories': self.instance.get_history_items(self.request)
        }
        context.update(kwargs)
        return super().get_context_data(**context)


class RequestOrderApproveView(ModelFormView, InstanceSpecificView):
    page_title = _('Approving')

    @cached_property
    def edit_url(self):
        return self.url_helper.get_action_url('approve', self.pk_quoted)

    def check_action_permitted(self, user):
        return self.permission_helper.user_can('approve', user, self.instance)

    def get_edit_handler(self):
        edit_handler = self.model_admin.approve_edit_handler
        return edit_handler.bind_to(model=self.model_admin.model)

    def get_instance(self):
        instance = super().get_instance()
        return instance

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_meta_title(self):
        return _('Approving %s') % self.verbose_name

    def get_success_message(self, instance):
        return _("%(model_name)s '%(instance)s' updated.") % {
            'model_name': capfirst(self.verbose_name), 'instance': instance
        }

    def get_context_data(self, **kwargs):
        context = {
            'user_can_delete': self.permission_helper.user_can_delete_obj(
                self.request.user, self.instance)
        }
        context.update(kwargs)
        return super().get_context_data(**context)

    def get_error_message(self):
        name = self.verbose_name
        return _("The %s could not be saved due to errors.") % name

    def get_template_names(self):
        return self.model_admin.get_edit_template()

    @transaction.atomic
    def form_valid(self, form):
        instance = form.save()
        # update stock_on_request for lock requestable stock
        instance.update_on_request_stock()
        instance.approve(self.request.user)
        messages.success(self.request, self.get_success_message(instance))
        return redirect(self.get_success_url())
