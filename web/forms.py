from datetime import timedelta

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

class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'description','max_player_per_team', 'game', 'max_teams', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            valorant = Game.objects.get(name__iexact="Valorant")
            self.fields['game'].initial = valorant.pk
        except Game.DoesNotExist:
            pass  # No pasa nada si no existe

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        # Comprobación para la fecha de inicio
        if not start_date:
            self.add_error('start_date', 'Debes introducir la fecha de inicio del torneo.')
        elif start_date < timezone.now() + timedelta(days=1):
            self.add_error('start_date', 'La fecha de inicio debe ser al menos 1 día después de la fecha actual.')

        # Comprobación para la fecha de finalización
        if not end_date:
            self.add_error('end_date', 'Debes introducir la fecha de fin del torneo.')

        if start_date and end_date:
            if end_date < start_date + timedelta(hours=1):
                self.add_error('end_date', 'La fecha de finalización debe ser como minimo 1 hora posterior a la fecha de inicio.')

        return cleaned_data


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
        }

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = [
            'first_name', 'last_name', 'birth_date', 'country',
            'bio', 'avatar'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-select'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Cuéntanos algo sobre ti...'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'birth_date': 'Fecha de nacimiento',
            'country': 'País',
            'bio': 'Biografía',
            'avatar': 'Avatar',
        }

class TournamentFilterForm(forms.Form):
    game = forms.ModelChoiceField(
        queryset=Game.objects.all(),
        required=False,
        empty_label="Todos los juegos",
        widget=forms.Select(attrs={'class': 'form-select bg-darker border-secondary text-light'})
    )
    status = forms.ChoiceField(
        choices=[('', 'Todos los estados'), ('open', 'Inscripciones abiertas'), ('ongoing', 'En progreso'), ('finished', 'Finalizados')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select bg-darker border-secondary text-light'})
    )
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control bg-darker border-secondary text-light', 'placeholder': 'Buscar torneos...'})
    )