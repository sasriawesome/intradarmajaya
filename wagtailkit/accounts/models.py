import uuid
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group
from allauth.account.signals import user_signed_up, email_confirmed

from wagtail.admin.edit_handlers import TabbedInterface, FieldPanel, MultiFieldPanel, ObjectList
from wagtail.contrib.settings.models import BaseSetting, register_setting


class User(AbstractUser):
    """ Custom User Model """

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4,
        editable=False, verbose_name=_('UUID'))

    @property
    def is_person(self):
        person = getattr(self, 'person', None)
        return bool(person)

    @property
    def fullname(self):
        person = getattr(self, 'person', None)
        name = self.get_full_name()
        if person:
            name = person.fullname
        return name

    @property
    def is_admin(self):
        return self.is_superuser

    def __str__(self):
        fname = self.username if self.fullname in [None, ''] else self.fullname
        return fname

    @staticmethod
    @receiver(user_signed_up)
    def after_user_signed_up(request, user, **kwargs):
        user.is_active = False
        user.save()

    @staticmethod
    @receiver(email_confirmed)
    def after_email_confirmed(request, email_address, **kwargs):
        user = email_address.user
        user.is_active = True
        user.save()


class AccountSetting(BaseSetting):
    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')

    user_registration_enabled = models.BooleanField(
        default=True, verbose_name=_('User registration enabled'),
        help_text=_('Activate user registration form'))
    default_new_user_group = models.ForeignKey(
        Group, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name=_('Registration default group'),
        help_text=_('Include new registered user to this group'))
    auto_create_person = models.BooleanField(
        default=True, verbose_name=_('Auto create person'),
        help_text=_('Create person data for new user created'))

    login_with_twitter = models.BooleanField(
        default=True, verbose_name=_('Login with Twitter'),
        help_text=_('Activate login with Twitter'))
    login_with_facebook = models.BooleanField(
        default=True, verbose_name=_('Login with Facebook'),
        help_text=_('Activate login with Facebook'))
    login_with_google = models.BooleanField(
        default=True, verbose_name=_('Login with Google'),
        help_text=_('Activate login with Google'))
    login_with_github = models.BooleanField(
        default=True, verbose_name=_('Login with Github'),
        help_text=_('Activate login with Github'))
    login_with_slack = models.BooleanField(
        default=True, verbose_name=_('Login with Slack'),
        help_text=_('Activate login with Slack'))

    registration_panels = [
        MultiFieldPanel([
            FieldPanel('user_registration_enabled'),
            FieldPanel('default_new_user_group'),
            FieldPanel('auto_create_person'),
        ], heading=_('Registration'))
    ]

    social_login_panels = [
        MultiFieldPanel([
            FieldPanel('login_with_twitter'),
            FieldPanel('login_with_facebook'),
            FieldPanel('login_with_google'),
            FieldPanel('login_with_github'),
            FieldPanel('login_with_slack'),
        ], heading=_('Registration'))
    ]

    edit_handler = TabbedInterface([
        ObjectList(registration_panels, heading=_('Registration'), help_text=_('New user registration setting')),
        ObjectList(social_login_panels, heading=_('Social Login'), help_text=_('Activate social authentication')),
    ])


register_setting(AccountSetting, icon='fa-user')
