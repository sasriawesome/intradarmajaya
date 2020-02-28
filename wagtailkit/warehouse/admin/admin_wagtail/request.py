from django.db import models
from django.contrib.admin.utils import quote
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _

from wagtail.admin.messages import messages
from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel,
    RichTextFieldPanel, TabbedInterface, ObjectList)
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtailkit.autocompletes.edit_handlers import AutocompletePanel
from wagtailkit.admin.views import CreateView
from wagtailkit.admin.admin import StatusModelAdminMixin
from wagtailkit.printpdf.admin import PrintPDFModelAdminMixin
from wagtailkit.warehouse.models import RequestOrder

from .helpers import RequestOrderPermissionHelper, RequestOrderButtonHelper
from .views import RequestOrderApproveView


class RequestOrderModelAdmin(PrintPDFModelAdminMixin, StatusModelAdminMixin):
    model = RequestOrder
    menu_label = _('Requests')
    menu_icon = 'doc-full'
    search_fields = ['inner_id', 'requester.name']
    list_per_page = 20
    list_filter = ['date_created', 'status', 'critical_status']
    list_display = ['inner_id', 'creator', 'requester', 'date_created', 'status']
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
            # FieldPanel('requester'),
            # FieldPanel('department'),
            # FieldPanel('deliver_to'),
            FieldPanel('critical_status'),
            FieldPanel('deadline'),
            FieldPanel('title'),
            RichTextFieldPanel('description'),
        ]),
    ]

    create_inventory_panel = [
        InlinePanel(
            'requested_inventories',
            panels=[
                AutocompletePanel('product'),
                FieldPanel('quantity_requested'),
            ]
        ),
    ]

    create_asset_panel = [
        InlinePanel(
            'requested_assets',
            panels=[
                AutocompletePanel('product'),
                FieldPanel('quantity_requested'),
            ]
        ),
    ]

    create_new_product_panel = [
        InlinePanel(
            'requested_new_products',
            panels=[
                MultiFieldPanel([
                    # FieldPanel('slug'),
                    ImageChooserPanel('picture'),
                    FieldPanel('name'),
                    FieldPanel('quantity_requested'),
                    FieldPanel('description'),
                ])
            ]
        ),
    ]

    approve_inventory_panel = [
        InlinePanel(
            'requested_inventories',
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
            'requested_assets',
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
            'requested_new_products',
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
        user_can_view_other = ph.can_view_other(request.user)
        if superuser or user_can_view_other:
            return qs
        else:
            return qs.filter(
                models.Q(creator=request.user)
                | models.Q(requester__in=request.user.person.employee.position.get_children())
            )

    def validate_view(self, request, instance_pk):
        # Set status
        instance = get_object_or_404(self.model, pk=instance_pk)
        perm_helper = self.permission_helper
        has_perm = perm_helper.user_can_validate_obj(request.user, instance)
        try:
            if has_perm:
                instance.validate()
                return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))
        except Exception as err:
            messages.add_message(request, messages.ERROR, err)
            return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))

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
