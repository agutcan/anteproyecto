# Formularios Clave

## Explicación de formularios en Django (`forms.py`)

Este archivo describe el propósito y funcionamiento de los formularios definidos para la aplicación web, utilizando Django Forms y ModelForms.

---

### 🧾 `CustomUserCreationForm`

Formulario personalizado para el registro de usuarios. Extiende de `UserCreationForm` e incluye:

* Campo `email` requerido.
* Campo de `aceptación de las políticas de privacidad y terminos de uso` requerido.
* Validaciones personalizadas para contraseña y campos obligatorios.

```python
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    error_messages = {
        "password_mismatch": ("Las contraseñas no coinciden"),
    }
    accept_privacy_policy_and_terms_of_use = forms.BooleanField(
        required=True,
        label="Acepto las Políticas de Privacidad y terminos de uso",
        error_messages={"required": "Debes aceptar las políticas de privacidad y los terminos de uso para registrarte."}
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
```

---

### 🏆 `TournamentForm`

Formulario para crear torneos, basado en el modelo `Tournament`. Incluye:

* Campos: `name`, `description`, `max_player_per_team`, `game`, `max_teams`, `start_date`.
* Widget personalizado para la fecha (`datetime-local`).
* Asigna por defecto el juego "Valorant" si existe.
* Valida que la fecha de inicio sea al menos un día posterior a la actual.

```python
class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'description','max_player_per_team', 'game', 'max_teams', 'start_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            valorant = Game.objects.get(name__iexact="Valorant")
            self.fields['game'].initial = valorant.pk
        except Game.DoesNotExist:
            pass

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        if not start_date:
            self.add_error('start_date', 'Debes introducir la fecha de inicio del torneo.')
        elif start_date < timezone.now() + timedelta(days=1):
            self.add_error('start_date', 'La fecha de inicio debe ser al menos 1 día después de la fecha actual.')
        return cleaned_data
```

---

### 👥 `TeamForm`

Formulario simple para crear equipos.

* Campo `name` para introducir el nombre del equipo, obligatorio.


```python
class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
        }
```

---

### 🧑‍💼 `PlayerForm`

Formulario para modificar el perfil de los jugadores.

* Campo `first_name` para introducir el nombre, no es obligatorio.
* Campo `last_name` para introducir el/los apellido/s, no es obligatorio.
* Campo `birth_date` para introducir la fecha de nacimiento, no es obligatorio.
* Campo `country` para introducir la ciudad, no es obligatorio.
* Campo `bio` para introducir una descripción, no es obligatorio.
* Campo `avatar` para introducir un avatar, no es obligatorio.


```python
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
```

---

### 🔍 `TournamentFilterForm`

Formulario para filtrar torneos.

* Campo `game` para filtrar por juego, no es obligatorio.
* Campo `status` para filtrar por estado, no es obligatorio.
* Campo `search` para filtrar por nombre, no es obligatorio.

```python
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
```

---

### 📩 `SupportForm`

Formulario de contacto o soporte.

* Campo `email` para introducir un email, obligatorio.
* Campo `subject` para introducir el titulo del problema/mensaje, obligatorio.
* Campo `message` para introducir el problema/mensaje, obligatorio.
* Campo `attach_file` para introducir una imagen, no es obligatorio.


```python
class SupportForm(forms.Form):
    email = forms.EmailField(
        label="Tu correo electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@correo.com'
        }),
        error_messages={
            'invalid': 'Ingresa un correo electrónico válido'
        }
    )

    subject = forms.CharField(
        label="Asunto",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Problema con torneo...'
        })
    )

    message = forms.CharField(
        label="Mensaje",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Describe tu problema o consulta en detalle...'
        })
    )

    attach_file = forms.FileField(
        label="Adjuntar archivo (opcional)",
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control'
        })
    )
```

---

### 🏋️ `MatchResultForm`

Formulario para registrar el resultado de un partido.

* Campo `winner` para introducir el equipo ganador, obligatorio.
* Campo `team1_score` para introducir la puntuación del primer equipo, obligatorio.
* Campo `team2_score` para introducir la puntuación del segundo equipo, obligatorio.

```python
class MatchResultForm(forms.Form):
    winner = forms.ChoiceField(
        choices=[('team1', 'Equipo 1'), ('team2', 'Equipo 2')],
        widget=forms.RadioSelect
    )
    team1_score = forms.IntegerField(min_value=0)
    team2_score = forms.IntegerField(min_value=0)
```

---

Estos formularios permiten construir interfaces limpias, seguras y fáciles de usar para crear y administrar torneos, usuarios y equipos dentro de la aplicación.

## 🔄 Navegación
[⬅️ Volver al README principal](../README.md)
