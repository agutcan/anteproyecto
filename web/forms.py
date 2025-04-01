from django.contrib.auth.forms import UserCreationForm
from django import forms
from web.models import *


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    error_messages = {
        "password_mismatch": ("Las contraseñas no coinciden"),
    }
    accept_privacy_policy = forms.BooleanField(
        required=True,
        label="Acepto las Políticas de Privacidad",
        error_messages={"required": "Debes aceptar las políticas de privacidad para registrarte."}
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user
