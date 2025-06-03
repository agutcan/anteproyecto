# 🧾 Formularios Clave

## ✍️ Explicación de formularios en Django (`forms.py`)

Este archivo describe el propósito y funcionamiento de los formularios definidos para la aplicación web, utilizando Django Forms y ModelForms.

---

### 👤 `CustomUserCreationForm` — Registro de Usuario

Formulario personalizado para el registro de usuarios. Extiende de `UserCreationForm` e incluye:

- ✅ Campo `email` requerido.
- ✅ Aceptación obligatoria de políticas y términos. 
- ✅ Validaciones personalizadas para contraseñas y campos obligatorios.

```python
class CustomUserCreationForm(UserCreationForm):
    """Formulario personalizado para la creación de usuarios.
    
    Extiende UserCreationForm para añadir campos adicionales y personalizar mensajes de error.
    
    Atributos:
        email (EmailField): Campo requerido para el email del usuario
        error_messages (dict): Mensajes de error personalizados
        accept_privacy_policy_and_terms_of_use (BooleanField): 
            Aceptación de términos requerida para el registro
    """
    
    email = forms.EmailField(required=True)
    
    error_messages = {
        "password_mismatch": ("Las contraseñas no coinciden"),
    }
    
    accept_privacy_policy_and_terms_of_use = forms.BooleanField(
        required=True,
        error_messages={
            "required": "Debes aceptar las políticas de privacidad y términos de uso para registrarte."
        }
    )

    class Meta:
        """Configuración del formulario base.
        
        Atributos:
            model: Modelo User al que está asociado el formulario
            fields: Campos incluidos en el formulario
        """
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        """Guarda el usuario asegurando que el email se almacene correctamente.
        
        Args:
            commit (bool): Si se debe guardar el usuario en la base de datos
            
        Returns:
            User: El objeto usuario creado
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
```

---

### 🏆 `TournamentForm` — Crear Torneos

Formulario basado en el modelo `Tournament`. Incluye:

- 🎮 Campos: `name`, `description`, `max_player_per_team`, `game`, `max_teams`, `start_date`.
- 🗓️ Widget personalizado para fecha (`datetime-local`).  
- 🛡️ Juego "Valorant" como valor por defecto (si existe).  
- ⏳ Valida que la fecha de inicio sea al menos 1 día posterior a la actual.

```python
class TournamentForm(forms.ModelForm):
    """Formulario para la creación/edición de torneos.
    
    Atributos:
        Meta.model: Modelo Tournament asociado al formulario
        Meta.fields: Campos incluidos en el formulario
        Meta.widgets: Widgets personalizados para los campos
    """
    class Meta:
        model = Tournament
        fields = ['name', 'description', 'max_player_per_team', 'game', 'max_teams', 'start_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        """Inicializa el formulario estableciendo Valorant como juego predeterminado si existe."""
        super().__init__(*args, **kwargs)
        try:
            valorant = Game.objects.get(name__iexact="Valorant")
            self.fields['game'].initial = valorant.pk
        except Game.DoesNotExist:
            pass  # No pasa nada si no existe

    def clean(self):
        """Validación personalizada para los datos del formulario.
        
        Realiza:
        - Validación de fecha de inicio (no puede ser vacía)
        - Validación de que la fecha sea al menos 1 día en el futuro
        """
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')

        # Comprobación para la fecha de inicio
        if not start_date:
            self.add_error('start_date', 'Debes introducir la fecha de inicio del torneo.')
        elif start_date < timezone.now() + timedelta(days=1):
            self.add_error('start_date', 'La fecha de inicio debe ser al menos 1 día después de la fecha actual.')

        return cleaned_data
```

---

### 👥 `TeamForm` — Crear Equipos

Formulario simple para crear equipos.

- 📝 Campo `name` obligatorio, con estilos personalizados.


```python
class TeamForm(forms.ModelForm):
    """Formulario para la creación/edición de equipos.
    
    Atributos:
        Meta.model: Modelo Team asociado al formulario
        Meta.fields: Campos incluidos en el formulario (solo nombre)
        Meta.widgets: Personalización del widget para el campo name
    """
    
    class Meta:
        model = Team
        fields = ['name']  # Solo incluye el campo 'name' del modelo Team
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary'  # Clases BOOSTRAP para estilizado
            }),
        }
```

---

### 🧑‍💼 `PlayerForm` — Perfil de Jugador

Formulario para modificar el perfil de los jugadores.

- 🧍 Campos:  `first_name`, `last_name`, `birth_date`, `country`, `bio`, `avatar`.  
- 🖼️ Todos los campos son opcionales.  
- 🧩 Widgets personalizados para mejorar la experiencia de usuario.


```python
class PlayerForm(forms.ModelForm):
    """Formulario para la edición del perfil de jugador.
    
    Permite actualizar:
    - Información personal (nombre, apellido, fecha nacimiento)
    - Datos de perfil (país, biografía, avatar)
    
    Atributos:
        Meta.model: Modelo Player asociado
        Meta.fields: Campos editables del perfil
        Meta.widgets: Configuración de los inputs del formulario
        Meta.labels: Etiquetas personalizadas para los campos
    """
    
    class Meta:
        model = Player
        fields = [
            'first_name', 'last_name', 'birth_date', 
            'country', 'bio', 'avatar'
        ]
        
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Apellido'
            }),
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'country': forms.Select(attrs={
                'class': 'form-select'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Cuéntanos algo sobre ti...'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            }),
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

### 🔍 `TournamentFilterForm` — Filtros de Torneos

Formulario para filtrar torneos.

- 🎮 Campos:  `game`, `status`, `search`

Todos los campos son opcionales.

```python
class TournamentFilterForm(forms.Form):
    """Formulario de filtrado para torneos con opciones de:
    - Filtrado por juego
    - Filtrado por estado
    - Búsqueda por texto
    
    Atributos:
        game (ModelChoiceField): Selector de juegos disponibles
        status (ChoiceField): Selector de estados del torneo
        search (CharField): Campo de búsqueda textual
    """
    
    game = forms.ModelChoiceField(
        queryset=Game.objects.all(),
        required=False,
        empty_label="Todos los juegos",
        widget=forms.Select(attrs={
            'class': 'form-select bg-darker border-secondary text-light'
        })
    )
    
    status = forms.ChoiceField(
        choices=[
            ('', 'Todos los estados'), 
            ('upcoming', 'Inscripciones abiertas'), 
            ('ongoing', 'En progreso'), 
            ('finished', 'Finalizados')
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select bg-darker border-secondary text-light'
        })
    )
    
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-darker border-secondary text-light', 
            'placeholder': 'Buscar torneos...'
        })
    )

```

---

### 📩 `SupportForm` — Contacto/Soporte

Formulario de contacto.

- 📧 Campos: `email`, `subject`, `message`, `attach_file`.


```python
class SupportForm(forms.Form):
    """Formulario de contacto para soporte técnico o consultas.
    
    Campos:
        email (EmailField): Correo del usuario para respuesta
        subject (CharField): Asunto del mensaje
        message (CharField): Contenido detallado de la consulta
        attach_file (FileField): Archivo adjunto opcional
    """
    
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

### 🏋️ `MatchResultForm` — Resultado de Partidos

Formulario para registrar el resultado de un partido.

- 🏆 Campos:  `winner`, `team1_score`, `team2_score`.

```python
class MatchResultForm(forms.Form):
    """Formulario para registrar los resultados de un partido.
    
    Campos:
        winner (ChoiceField): Selección del equipo ganador
        team1_score (IntegerField): Puntuación del equipo 1
        team2_score (IntegerField): Puntuación del equipo 2
    """
    
    winner = forms.ChoiceField(
        choices=[('team1', 'Equipo 1'), ('team2', 'Equipo 2')],
        widget=forms.RadioSelect,
        label="Equipo ganador"
    )
    
    team1_score = forms.IntegerField(
        min_value=0,
        label="Puntuación Equipo 1"
    )
    
    team2_score = forms.IntegerField(
        min_value=0,
        label="Puntuación Equipo 2"
    )
```

## 🔄 Navegación

- ️🏗️ [Estructura del Proyecto y esquema de base de datos](PROJECT_STRUCTURE.md)
- ⚙️ [Admin](ADMIN.md)
- 🖼️ [Vistas](VIEWS.md)
- ⏰ [Tareas programadas](TASKS.md)
- 🧩 [Modelos](MODELS.md)
- 📝 [Formularios](FORMS.md)
- ✅ [Test](TESTS.md)
- 🔄 [Serializadores](SERIALIZERS.md)
- 🧠 [Funciones](FUNCTIONS.md)
- ⬅️ [Volver al README principal](../README.md)
