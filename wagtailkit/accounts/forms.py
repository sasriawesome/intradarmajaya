from django import forms
from allauth import app_settings
from allauth.account.forms import LoginForm, ResetPasswordForm, SignupForm, ChangePasswordForm, AddEmailForm
from django.utils.translation import gettext_lazy as _

auht_settings = app_settings.settings


class AuthenticationMethod:
    USERNAME = 'username'
    EMAIL = 'email'
    USERNAME_EMAIL = 'username_email'


class AccountAuthenticationForm(LoginForm):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'id': 'inputPassword',
                'placeholder': _('******'),
                'class': 'form-control form-control-sm'
            }
        ),
    )
    remember = forms.BooleanField(
        label=_("Remember Me"),
        required=False,
        widget=forms.CheckboxInput(attrs={
            'id': 'remember',
            'class': 'custom-control-input'
        })
    )

    def __init__(self, request=None, *args, **kwargs):
        kwargs['request'] = request
        super(AccountAuthenticationForm, self).__init__(*args, **kwargs)
        login_field = self.fields["login"]
        login_field.widget.attrs.update({
            'id': 'inputUsername',
            'class': 'form-control form-control-sm'
        })

    def login(self, *args, **kwargs):
        # Add your own processing here.
        # You must return the original result.
        return super(AccountAuthenticationForm, self).login(*args, **kwargs)


class AccountResetPasswordForm(ResetPasswordForm):
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'id': 'inputEmail',
                'placeholder': _('eg: youremail@site.com'),
                'class': 'form-control form-control-sm'
            }
        ))

class AccountSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(AccountSignupForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({'class': 'form-control form-control-sm'})
        self.fields["username"].widget.attrs.update({'class': 'form-control form-control-sm'})
        self.fields["password1"].widget.attrs.update({'class': 'form-control form-control-sm'})
        self.fields["password2"].widget.attrs.update({'class': 'form-control form-control-sm'})


class AccountChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super(AccountChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields["oldpassword"].widget.attrs.update({'class': 'form-control form-control-sm'})
        self.fields["password1"].widget.attrs.update({'class': 'form-control form-control-sm'})
        self.fields["password2"].widget.attrs.update({'class': 'form-control form-control-sm'})


class AccountAddEmailForm(AddEmailForm):
    def __init__(self, *args, **kwargs):
        super(AccountAddEmailForm, self).__init__(*args, **kwargs)
        self.fields["email"].label = _('Add more email')
        self.fields["email"].widget.attrs.update({'class': 'form-control form-control-sm'})
