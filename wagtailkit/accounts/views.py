from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.contrib.auth import views
from .forms import AccountAuthenticationForm, AccountResetPasswordForm


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)