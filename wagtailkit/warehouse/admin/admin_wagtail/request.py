from django.db import transaction
from django.contrib.admin.utils import quote, capfirst
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property

from wagtail.admin.messages import messages
from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, RichTextFieldPanel, TabbedInterface, ObjectList)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.modeladmin.views import ModelFormView, InstanceSpecificView
from wagtailautocomplete.edit_handlers import AutocompletePanel

from wagtailkit.admin.views import CreateView
from wagtailkit.admin.admin import StatusModelAdminMixin
from wagtailkit.admin.helpers import PermissionHelper, StatusButtonHelper
from wagtailkit.printpdf.admin import PrintPDFModelAdminMixin
from wagtailkit.printpdf.helpers import PrintPDFButtonHelperMixin
from wagtailkit.warehouse.models import RequestOrder


class RequestOrderPermissionHelper(PermissionHelper):
    """ Request Order PermissionHelper """

    def user_can_edit_obj(self, user, obj):
        can_change = self.user_can('change', user)
        can_change_other = self.user_can('changeother', user)
        is_editable = getattr(obj, 'is_editable', None)
        if user.is_superuser:
            return True
        if can_change_other and is_editable:
            return True
        if self.is_owner(user, obj) and can_change and is_editable:
            return True
        else:
            return False

    def user_can_inspect_obj(self, user, obj):
        has_perm = self.inspect_view_enabled and self.user_has_any_permissions(user)
        can_view_other = self.user_can('viewother', user, obj)
        if user.is_superuser:
            return True
        if can_view_other and has_perm:
            return True
        if self.is_owner(user, obj) and has_perm:
            return True
        else:
            return False


class RequestOrderButtonHelper(PrintPDFButtonHelperMixin, StatusButtonHelper):
    # Exclude action
    buttons_exclude = ['process', 'complete', 'close']


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
        instance.approved_by = self.request.user
        instance.date_approved = timezone.now()
        instance.status = self.model.APPROVED
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
        messages.success(self.request, self.get_success_message(instance))
        return redirect(self.get_success_url())


class RequestOrderModelAdmin(PrintPDFModelAdminMixin, StatusModelAdminMixin):
    model = RequestOrder
    menu_label = _('Requests')
    menu_icon = 'doc-full'
    search_fields = ['inner_id', 'requester']
    list_per_page = 20
    list_filter = ['date_created', 'status', 'critical_status']
    list_display = ['inner_id', 'requester', 'date_created', 'status']
    inspect_view_enabled = True
    permission_helper_class = RequestOrderPermissionHelper
    approve_view_class = RequestOrderApproveView
    button_helper_class = RequestOrderButtonHelper
    create_view_class = CreateView
    detail_document_title = _('Request Order')
    index_document_title = _('Request Order')

    order_panel = [
        MultiFieldPanel([
            # FieldPanel('status'),
            FieldPanel('requester'),
            FieldPanel('deliver_to'),
            FieldPanel('department'),
            FieldPanel('critical_status'),
            FieldPanel('deadline'),
            FieldPanel('title'),
            RichTextFieldPanel('description'),
        ], heading=_('Information')),
    ]

    create_inventory_panel = [
        InlinePanel(
            'requested_inventories', label=_('Inventory'),
            panels=[
                AutocompletePanel('product'),
                FieldRowPanel([
                    FieldPanel('quantity_requested'),
                ]),
            ]
        ),
    ]

    create_asset_panel = [
        InlinePanel(
            'requested_assets', label=_('Asset'),
            panels=[
                AutocompletePanel('product'),
                FieldRowPanel([
                    FieldPanel('quantity_requested'),
                ]),
            ]
        ),
    ]

    create_new_product_panel = [
        InlinePanel(
            'requested_new_products', label=_('New Product'),
            panels=[
                MultiFieldPanel([
                    ImageChooserPanel('picture'),
                    # FieldPanel('slug'),
                    FieldPanel('name'),
                    FieldPanel('quantity_requested'),
                    FieldPanel('description'),
                ])
            ]
        ),
    ]

    approve_inventory_panel = [
        InlinePanel(
            'requested_inventories', label=_('Inventories'),
            panels=[
                FieldPanel('product'),
                FieldRowPanel([
                    FieldPanel('quantity_requested'),
                    FieldPanel('quantity_approved'),
                ]),
            ]
        ),
    ]

    approve_asset_panel = [
        InlinePanel(
            'requested_assets', label=_('Assets'),
            panels=[
                FieldPanel('product'),
                FieldRowPanel([
                    FieldPanel('quantity_requested'),
                    FieldPanel('quantity_approved'),
                ]),
            ]
        ),
    ]

    approve_new_product_panel = [
        InlinePanel(
            'requested_new_products', label=_('New Product'),
            panels=[
                MultiFieldPanel([
                    ImageChooserPanel('picture'),
                    FieldPanel('name'),
                    FieldPanel('quantity_requested'),
                    FieldPanel('quantity_approved'),
                    FieldPanel('description'),
                ])
            ]
        ),
    ]

    edit_handler = TabbedInterface([
        ObjectList(order_panel, heading=_('Request')),
        ObjectList(create_inventory_panel, heading=_('Inventory')),
        ObjectList(create_asset_panel, heading=_('Asset')),
        ObjectList(create_new_product_panel, heading=_('New Product')),
    ])

    approve_edit_handler = TabbedInterface([
        ObjectList(approve_inventory_panel, heading=_('Inventory')),
        ObjectList(approve_asset_panel, heading=_('Asset')),
        ObjectList(approve_new_product_panel, heading=_('New Product')),
    ])

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        ph = self.permission_helper
        superuser = request.user.is_superuser
        can_view_other = ph.can_view_other(request.user)
        print(can_view_other)
        if superuser or can_view_other:
            return qs
        else:
            return qs.filter(creator=request.user)

    def approve_view(self, request, instance_pk):
        kwargs = {'model_admin': self, 'instance_pk': instance_pk}
        view_class = self.approve_view_class
        return view_class.as_view(**kwargs)(request)

    def reject_view(self, request, instance_pk):
        # Set status
        instance = get_object_or_404(self.model, pk=instance_pk)
        codename = 'reject'
        perm_helper = self.permission_helper
        superuser = request.user.is_superuser
        has_perm = perm_helper.user_can(codename, request.user, instance)
        try:
            if superuser or has_perm:
                getattr(instance, codename)()
                return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))
        except Exception as err:
            messages.add_message(request, messages.ERROR, err)
            return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))
