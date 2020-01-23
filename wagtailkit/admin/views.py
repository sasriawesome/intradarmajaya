from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from wagtail.admin import messages
from wagtail.contrib.modeladmin.views import (
    CreateView as CreateViewBase,
    EditView as EditViewBase,
    InspectView as InspectViewBase
)


class InspectView(InspectViewBase):
    """ Custom ModelAdmin Inspect View """


class EditView(EditViewBase):
    """ Custom ModelAdmin Inspect View """

    def form_valid(self, form):
        # TODO Catch Validation Error
        # Wagtail inline uncontrolled exeption
        try:
            instance = form.save()
            messages.success(
                self.request, self.get_success_message(instance),
                buttons=self.get_success_message_buttons(instance))
            return redirect(self.get_success_url())
        except ValidationError as err:
            messages.validation_error(
                self.request, err.messages[0], form
            )
            return self.render_to_response(self.get_context_data())

class CreateView(CreateViewBase):
    """ Custom ModelAdmin Create View """

    def get_instance(self):
        instance = super().get_instance()
        instance.creator = self.request.user
        return instance

    def form_valid(self, form):
        # TODO Catch Validation Error
        # Wagtail inline uncontrolled exeption
        try:
            instance = form.save()
            messages.success(
                self.request, self.get_success_message(instance),
                buttons=self.get_success_message_buttons(instance))
            return redirect(self.get_success_url())
        except ValidationError as err:
            messages.validation_error(
                self.request, err.messages[0], form
            )
            return self.render_to_response(self.get_context_data())