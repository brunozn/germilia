from django import forms
from django.contrib.auth.forms import AuthenticationForm


class SignInForm(AuthenticationForm):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={
        'placeholder': 'Usuario', 'class': "form-control",
    }))

    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={
        'placeholder': 'Senha', 'class': "form-control",
    }))
