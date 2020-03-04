from django.contrib.admin.utils import quote, capfirst
from django.conf.urls import url
from django.shortcuts import get_object_or_404, redirect, reverse

from wagtail.admin.messages import messages
from wagtail.contrib.modeladmin.options import ModelAdmin

from wagtailkit.admin.helpers import StatusButtonHelper


class StatusModelAdminMixin(ModelAdmin):
    """ Add URL and view for status mixin """

    button_helper_class = StatusButtonHelper

    def get_admin_urls_for_registration(self):
        urls = super().get_admin_urls_for_registration()
        added_urls = (
            url(self.url_helper.get_action_url_pattern('trash'),
                self.trash_view, name=self.url_helper.get_action_url_name('trash')),
            url(self.url_helper.get_action_url_pattern('draft'),
                self.draft_view, name=self.url_helper.get_action_url_name('draft')),
            url(self.url_helper.get_action_url_pattern('validate'),
                self.validate_view, name=self.url_helper.get_action_url_name('validate')),
            url(self.url_helper.get_action_url_pattern('approve'),
                self.approve_view, name=self.url_helper.get_action_url_name('approve')),
            url(self.url_helper.get_action_url_pattern('reject'),
                self.reject_view, name=self.url_helper.get_action_url_name('reject')),
            url(self.url_helper.get_action_url_pattern('process'),
                self.process_view, name=self.url_helper.get_action_url_name('process')),
            url(self.url_helper.get_action_url_pattern('complete'),
                self.complete_view, name=self.url_helper.get_action_url_name('complete')),
            url(self.url_helper.get_action_url_pattern('close'),
                self.close_view, name=self.url_helper.get_action_url_name('close')),
        )
        return added_urls + urls

    def trash_view(self, request, instance_pk):
        # Set status
        instance = get_object_or_404(self.model, pk=instance_pk)
        codename = 'trash'
        perm_helper = self.permission_helper
        has_perm = perm_helper.user_can(codename, request.user, instance)
        is_owner = perm_helper.is_owner(request.user, instance)
        can_change_other = perm_helper.can_change_other(request.user)
        try:
            if can_change_other or has_perm and is_owner:
                getattr(instance, codename)(request.user)
                return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))
        except Exception as err:
            messages.add_message(request, messages.ERROR, err)
            return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))

    def draft_view(self, request, instance_pk):
        # Set status to draft
        instance = get_object_or_404(self.model, pk=instance_pk)
        codename = 'draft'
        perm_helper = self.permission_helper
        has_perm = perm_helper.user_can(codename, request.user, instance)
        is_owner = perm_helper.is_owner(request.user, instance)
        can_change_other = perm_helper.can_change_other(request.user)
        try:
            if can_change_other or has_perm and is_owner:
                getattr(instance, codename)()
                return redirect(reverse(self.url_helper.get_action_url_name('inspect'), args=(instance_pk,)))
        except Exception as err:
            messages.add_message(request, messages.ERROR, err)
            return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))

    def validate_view(self, request, instance_pk):
        # Set status
        codename = 'validate'
        instance = get_object_or_404(self.model, pk=instance_pk)
        perm_helper = self.permission_helper
        has_perm = perm_helper.user_can(codename, request.user, instance)
        is_owner = perm_helper.is_owner(request.user, instance)
        can_change_other = perm_helper.can_change_other(request.user)
        try:
            if can_change_other or has_perm and is_owner:
                instance.validate(request.user)
                return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))
        except Exception as err:
            messages.add_message(request, messages.ERROR, err)
            return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))

    def approve_view(self, request, instance_pk):
        raise NotImplementedError

    def reject_view(self, request, instance_pk):
        raise NotImplementedError

    def process_view(self, request, instance_pk):
        # Set status
        instance = get_object_or_404(self.model, pk=instance_pk)
        codename = 'process'
        perm_helper = self.permission_helper
        has_perm = perm_helper.user_can(codename, request.user, instance)
        is_owner = perm_helper.is_owner(request.user, instance)
        can_change_other = perm_helper.can_change_other(request.user)
        try:
            if can_change_other or has_perm and is_owner:
                getattr(instance, codename)(request.user)
                return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))
        except Exception as err:
            messages.add_message(request, messages.ERROR, err)
            return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))

    def complete_view(self, request, instance_pk):
        raise NotImplementedError

    def close_view(self, request, instance_pk):
        # Set status
        instance = get_object_or_404(self.model, pk=instance_pk)
        codename = 'close'
        perm_helper = self.permission_helper
        has_perm = perm_helper.user_can(codename, request.user, instance)
        is_owner = perm_helper.is_owner(request.user, instance)
        can_change_other = perm_helper.can_change_other(request.user)
        if can_change_other or has_perm and is_owner:
            getattr(instance, codename)(request.user)
            return redirect(self.url_helper.get_action_url('inspect', quote(instance_pk)))
