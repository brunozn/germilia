from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UsernameField
from django.utils.translation import gettext_lazy as _


class SignInForm(AuthenticationForm):
    password = forms.CharField(label=_(""), widget=forms.PasswordInput(attrs={
        'placeholder': _('Password')
    }))
