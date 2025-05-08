# 🧾 Interfaz Admin

## ✍️ Explicación de admin en Django (`admin.py`)

Este archivo describe las configuraciones para la interfaz del admin de django.
---

### 🎮 Configuración del Admin para el Modelo `Game` 

Este archivo explica cómo configurar el panel de administración de Django para el modelo `Game`. La configuración personalizada se encuentra en la clase `GameAdmin`, la cual modifica la visualización, búsqueda, filtrado y presentación de las imágenes en el admin.

#### 📜 1. **Registro del Modelo en el Admin**

La clase `GameAdmin` se registra con el decorador `@admin.register(Game)`. Esto indica que `GameAdmin` se utilizará para configurar cómo se muestra el modelo `Game` en el panel de administración de Django.

#### 🗂️ 2. **Configuración de la Visualización de la Lista**

La opción `list_display` se usa para personalizar las columnas que se mostrarán en la lista de objetos dentro del admin. En este caso, se muestran los siguientes campos:

- 🎮 **Nombre del juego** : Muestra el nombre del juego.
- 🎭 **Género del juego** : Muestra el género asociado al juego.
- 🗓️ **Fecha de creación** : Muestra la fecha en la que se creó el juego.
- 🖼️ **Vista previa de la imagen** : Muestra una miniatura de la imagen del juego.
- 🌐 **URL de la imagen** : Muestra la URL completa de la imagen asociada al juego.

#### 🔍 3. **Configuración de la Búsqueda**

La opción `search_fields` permite definir qué campos serán utilizados para realizar búsquedas dentro del admin. En este caso, se puede buscar por el **nombre del juego** y por **género**.

#### ⚙️ 4. **Configuración de Filtros**

La opción `list_filter` agrega filtros en la barra lateral de la vista de lista. En este caso, se incluye un filtro para el **género del juego**, lo que permite filtrar los juegos según su categoría.

#### 🖼️ 5. **Método de Vista Previa de Imagen**

La función de **vista previa de imagen** genera una miniatura de la imagen del juego para mostrarla en el panel de administración. Si el objeto `Game` tiene una imagen asociada, se presenta una pequeña vista previa de la imagen. Si no hay imagen disponible, se muestra el texto **"No image"**.

##### Comportamiento:
- Si el juego tiene una imagen, se muestra una miniatura de 50x50 píxeles con bordes redondeados.
- Si no hay imagen, se muestra el mensaje **"No image"**.

##### Descripción de la columna:
El nombre de la columna en el panel de administración es **"Imagen"**.

#### 🌐 6. **Método de URL de la Imagen**

La función de **URL de la imagen** muestra la URL completa de la imagen asociada al juego. Si el objeto `Game` tiene una imagen, se muestra su URL. Si no existe imagen, se muestra el mensaje **"No image"**.

##### Comportamiento:
- Si el juego tiene una imagen, se presenta su URL completa.
- Si no hay imagen disponible, se muestra el mensaje **"No image"**.

##### Descripción de la columna:
El nombre de la columna en el panel de administración es **"Imagen URL"**.

```python
# Configuración del administrador para el modelo Game
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """Configuración personalizada para el modelo Game en el admin de Django.
    
    Personaliza la visualización y comportamiento de los equipos en el admin.
    """
    
    list_display = (
        'name',            # Nombre del juego
        'genre',          # Género del juego
        'created_at',     # Fecha de creación
        'image_preview',  # Vista previa de la imagen
        'image_url'       # URL de la imagen
    )
    
    search_fields = (
        'name',   # Búsqueda por nombre del juego
        'genre'   # Búsqueda por género
    )
    
    list_filter = (
        'genre',  # Filtro por género
    )

    def image_preview(self, obj):
        """Genera una miniatura de la imagen del juego para visualización en el admin.
        
        Args:
            obj: Instancia del modelo Game
            
        Returns:
            HTML con la imagen en miniatura o texto si no existe imagen
        """
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 5px;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = "Imagen"  # Nombre de columna en el admin

    def image_url(self, obj):
        """Muestra la URL completa de la imagen del juego.
        
        Args:
            obj: Instancia del modelo Game
            
        Returns:
            str: URL de la imagen o texto indicando ausencia
        """
        if obj.image:
            return obj.image.url
        return "No image"
    image_url.short_description = "Imagen URL"  # Nombre de columna en el admin
```

---

### 🏆 Configuración del Administrador para el Modelo `Tournament` 

Este archivo explica cómo configurar el panel de administración de Django para el modelo `Tournament`. La configuración personalizada se encuentra en la clase `TournamentAdmin`, la cual modifica la visualización, búsqueda, filtrado y otros aspectos del torneo en el admin.

#### 📜 1. **Registro del Modelo en el Admin**

La clase `TournamentAdmin` se registra con el decorador `@admin.register(Tournament)`. Esto indica que `TournamentAdmin` se utilizará para configurar cómo se muestra el modelo `Tournament` en el panel de administración de Django.

#### 🗂️ 2. **Configuración de la Visualización de la Lista**

La opción `list_display` se usa para personalizar las columnas que se mostrarán en la lista de objetos dentro del admin. En este caso, se muestran los siguientes campos:

- 🏆 **Nombre del torneo**: Muestra el nombre del torneo.
- 🎮 **Juego asociado**: Muestra el juego con el cual está relacionado el torneo.
- ⚙️ **Estado actual**: Muestra el estado actual del torneo (ej. "upcoming", "ongoing").
- 📝 **Descripción**: Muestra una breve descripción del torneo.
- 📅 **Fecha de inicio**: Muestra la fecha programada para el inicio del torneo.
- 👤 **Creador del torneo**: Muestra el nombre del usuario que creó el torneo.
- ⚔️ **Partidos generados**: Muestra si los partidos han sido generados.
- 🔢 **Máximo de equipos**: Muestra el número máximo de equipos que pueden participar.
- 👥 **Jugadores por equipo**: Muestra el número máximo de jugadores por equipo.
- 🏅 **Equipo ganador**: Muestra el equipo ganador (si ya se ha determinado).

#### 🔍 3. **Configuración de la Búsqueda**

La opción `search_fields` permite definir qué campos serán utilizados para realizar búsquedas dentro del admin. En este caso, se puede buscar por el **nombre del torneo**, el **nombre del juego asociado** y el **nombre de usuario del creador del torneo**.

#### ⚙️ 4. **Configuración de Filtros**

La opción `list_filter` agrega filtros en la barra lateral de la vista de lista. En este caso, se incluye un filtro por:

- **Estado del torneo**: Permite filtrar los torneos según su estado (por ejemplo, si está "upcoming" o "ongoing").
- **Juego asociado**: Permite filtrar los torneos según el juego con el que están asociados.

```python

# Configuración del administrador para el modelo Tournament
@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    """Configuración personalizada para el modelo Tournament en el admin de Django.
    
    Personaliza la visualización y comportamiento de los equipos en el admin.
    """
    
    list_display = (
        'name',              # Nombre del torneo
        'game',              # Juego asociado
        'status',            # Estado actual
        'description',       # Descripción 
        'start_date',        # Fecha de inicio
        'created_by',        # Creador del torneo
        'matches_generated', # Partidos generados
        'max_teams',         # Máximo de equipos
        'max_player_per_team',    # Jugadores por equipo
        'winner'             # Equipo ganador
    )
    
    search_fields = (
        'name',  # Búsqueda por nombre del equipo
        'game__name',  # Búsqueda por nombre del juego (relación)
        'created_by__username'  # Búsqueda por nombre de usuario del creador
    )
    
    list_filter = (
        'status',  # Filtro por estado del torneo
        'game'  # Filtro por juego asociado
    )

```
---
### 🏅 Configuración del Administrador para el Modelo `Team` 

Este archivo explica cómo configurar el panel de administración de Django para el modelo `Team`. La configuración personalizada se encuentra en la clase `TeamAdmin`, la cual modifica la visualización, búsqueda y ordenación de los equipos en el admin.

#### 📜 1. **Registro del Modelo en el Admin**

La clase `TeamAdmin` se registra con el decorador `@admin.register(Team)`. Esto indica que `TeamAdmin` se utilizará para configurar cómo se muestra el modelo `Team` en el panel de administración de Django.

#### 🗂️ 2. **Configuración de la Visualización de la Lista**

La opción `list_display` se usa para personalizar las columnas que se mostrarán en la lista de objetos dentro del admin. En este caso, se muestran los siguientes campos:

- 🏅 **Nombre del equipo**: Muestra el nombre del equipo.
- 🗓️ **Fecha de creación**: Muestra la fecha en la que se creó el equipo.
- 👤 **Líder**: Muestra el líder o capitán del equipo.
- 🔍 **Buscando compañeros**: Indica si el equipo está buscando nuevos miembros.

#### 🔍 3. **Configuración de la Búsqueda**

La opción `search_fields` permite definir qué campos serán utilizados para realizar búsquedas dentro del admin. En este caso, se puede buscar solo por el **nombre del equipo**.

#### 🔄 4. **Configuración de la Ordenación**

La opción `ordering` permite establecer el orden de los objetos en la vista de lista. En este caso, se ordenan los equipos de forma **descendente** por la **fecha de creación**, mostrando primero los más recientes.

```python
# Configuración del administrador para el modelo Team
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Configuración del panel de administración para el modelo Team.
    
    Personaliza la visualización y comportamiento de los equipos en el admin.
    """
    
    list_display = (
        'name',          # Nombre del equipo
        'created_at',    # Fecha de creación
        'leader',        # Líder/capitán del equipo
        'searching_teammates'  # Si está buscando miembros
    )
    
    search_fields = (
        'name',  # Búsqueda solo por nombre del equipo
    )
    
    ordering = (
        '-created_at',  # Orden descendente por fecha de creación
    )

```
---

### 🎮 Configuración del Administrador para el Modelo `Player` 

Este archivo explica cómo configurar el panel de administración de Django para el modelo `Player`. La configuración personalizada se encuentra en la clase `PlayerAdmin`, que modifica la visualización, edición, búsqueda y otros aspectos del jugador en el admin.

#### 📜 1. **Registro del Modelo en el Admin**

La clase `PlayerAdmin` se registra con el decorador `@admin.register(Player)`. Esto indica que `PlayerAdmin` se utilizará para configurar cómo se muestra el modelo `Player` en el panel de administración de Django.

#### 🗂️ 2. **Configuración de la Visualización de la Lista**

La opción `list_display` se usa para personalizar las columnas que se mostrarán en la lista de objetos dentro del admin. En este caso, se muestran los siguientes campos:

- 👤 **Usuario asociado**: Muestra el nombre de usuario asociado al jugador.
- 🏅 **Equipo actual**: Muestra el equipo al que pertenece el jugador.
- 🎭 **Rol**: Muestra el tipo de cuenta (Premium/Normal).
- 🌍 **País de origen**: Muestra el país del jugador.
- 💰 **Monedas virtuales**: Muestra las monedas que el jugador tiene.
- ⭐ **Renombre**: Muestra la puntuación de reputación del jugador.
- 📊 **MMR (Match Making Rating)**: Muestra el rating de matchmaking del jugador.
- 🏆 **Partidas jugadas**: Muestra el número total de partidas jugadas por el jugador.
- 🏅 **Partidas ganadas**: Muestra el número total de partidas ganadas por el jugador.
- 📈 **Winrate preview**: Muestra el porcentaje de victorias del jugador.
- 🖼️ **Vista previa del avatar**: Muestra una miniatura del avatar del jugador.
- 🌐 **URL del avatar**: Muestra la URL completa del avatar del jugador.

#### 🛠️ 3. **Configuración de la Edición de la Lista**

La opción `list_editable` permite especificar qué campos son editables directamente desde la vista de lista en el admin. En este caso, los campos editables son:

- 🎭 **Rol**: Permite cambiar el rol (Premium/Normal).
- 🌍 **País de origen**: Permite cambiar el país del jugador.
- 💰 **Monedas virtuales**: Permite editar las monedas.
- ⭐ **Renombre**: Permite editar la puntuación de reputación.

#### 🔍 4. **Configuración de la Búsqueda**

La opción `search_fields` permite definir qué campos serán utilizados para realizar búsquedas dentro del admin. En este caso, se puede buscar por:

- **Nombre de usuario** del jugador.
- **Nombre del equipo** al que pertenece el jugador.

#### ⚙️ 5. **Configuración de Filtros**

La opción `list_filter` permite agregar filtros en la barra lateral de la vista de lista. En este caso, se incluye un filtro por:

- **Rol**: Permite filtrar por tipo de cuenta (Premium/Normal).
- **Equipo**: Permite filtrar por el equipo al que pertenece el jugador.
- **País**: Permite filtrar por país de origen del jugador.

#### 📊 6. **Método de Winrate Preview**

La función de **winrate_preview** muestra el porcentaje de victorias (winrate) del jugador, formateado como un número entero sin decimales.

##### Comportamiento:
- Si el jugador tiene un winrate, se muestra como un porcentaje (ej. "75%").

##### Descripción de la columna:
El nombre de la columna en el panel de administración es **"Winrate"**.

#### 🖼️ 7. **Método de Vista Previa del Avatar**

La función de **avatar_preview** genera una miniatura del avatar del jugador para mostrarla en el panel de administración. Si el jugador tiene un avatar asociado, se muestra una pequeña imagen en miniatura. Si no tiene avatar, se muestra el mensaje **"No image"**.

##### Comportamiento:
- Si el jugador tiene un avatar, se muestra una miniatura de 50x50 píxeles con bordes redondeados.
- Si no hay avatar, se muestra el mensaje **"No image"**.

##### Descripción de la columna:
El nombre de la columna en el panel de administración es **"Avatar"**.

#### 🌐 8. **Método de URL del Avatar**

La función de **avatar_url** muestra la URL completa del avatar del jugador. Si el jugador tiene un avatar asociado, se muestra la URL. Si no tiene avatar, se muestra el mensaje **"No image"**.

##### Comportamiento:
- Si el jugador tiene un avatar, se presenta su URL completa.
- Si no hay avatar disponible, se muestra el mensaje **"No image"**.

##### Descripción de la columna:
El nombre de la columna en el panel de administración es **"Avatar URL"**.

```python
# Configuración del administrador para el modelo Player
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    """Configuración personalizada para el modelo Player en el admin de Django.
    
    Personaliza la visualización y comportamiento de los jugadores en el panel de administración.
    """
    
    list_display = (
        'user',            # Usuario asociado
        'team',            # Equipo actual
        'role',            # Rol (Premium/Normal)
        'country',         # País de origen
        'coins',           # Monedas virtuales
        'renombre',        # Puntuación de reputación
        'mmr',             # Match Making Rating
        'games_played',    # Partidas jugadas
        'games_won',       # Partidas ganadas
        'winrate_preview', # Winrate formateado
        'avatar_preview',  # Vista previa del avatar
        'avatar_url'       # URL del avatar
    )
    
    list_filter = (
        'role',    # Filtro por tipo de cuenta
        'team',    # Filtro por equipo
        'country'  # Filtro por país
    )
    
    search_fields = (
        'user__username',  # Búsqueda por nombre de usuario
        'team__name'       # Búsqueda por nombre de equipo
    )
    
    list_editable = (
        'role',     # Edición directa del rol
        'country',  # Edición directa del país
        'coins',    # Edición directa de las monedas
        'renombre'  # Edición directa del renombre
    )

    def winrate_preview(self, obj):
        """Muestra el winrate formateado como porcentaje sin decimales.
        
        Args:
            obj: Instancia del modelo Player
            
        Returns:
            str: Winrate formateado (ej: "75%")
        """
        return f"{obj.winrate:.0f}%"
    winrate_preview.short_description = 'Winrate'

    def avatar_preview(self, obj):
        """Genera una miniatura del avatar del jugador.
        
        Args:
            obj: Instancia del modelo Player
            
        Returns:
            HTML con la imagen en miniatura o texto si no existe avatar
        """
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 5px;" />',
                obj.avatar.url
            )
        return "No image"
    avatar_preview.short_description = "Avatar"

    def avatar_url(self, obj):
        """Muestra la URL completa del avatar.
        
        Args:
            obj: Instancia del modelo Player
            
        Returns:
            str: URL del avatar o texto indicando ausencia
        """
        if obj.avatar:
            return obj.avatar.url
        return "No image"
    avatar_url.short_description = "Avatar URL"
```
---

### 🎮🏆 Configuración del Administrador para el Modelo `TournamentTeam` 

Este archivo explica cómo configurar el panel de administración de Django para el modelo `TournamentTeam`. La configuración personalizada se encuentra en la clase `TournamentTeamAdmin`, que se encarga de personalizar la visualización, búsqueda y validación de la relación entre torneos y equipos.

#### 📜 1. **Registro del Modelo en el Admin**

La clase `TournamentTeamAdmin` se registra con el decorador `@admin.register(TournamentTeam)`. Esto indica que `TournamentTeamAdmin` se utilizará para configurar cómo se muestra el modelo `TournamentTeam` en el panel de administración de Django.

#### 🗂️ 2. **Configuración de la Visualización de la Lista**

La opción `list_display` se usa para personalizar las columnas que se mostrarán en la lista de objetos dentro del admin. En este caso, se muestran los siguientes campos:

- 🏆 **Torneo**: Muestra el nombre del torneo asociado al equipo.
- 🎮 **Equipo**: Muestra el nombre del equipo que está inscrito en el torneo.

#### 🔍 3. **Configuración de la Búsqueda**

La opción `search_fields` permite definir qué campos serán utilizados para realizar búsquedas dentro del admin. En este caso, se puede buscar por:

- **Nombre del torneo** al que está asociado el equipo.
- **Nombre del equipo** que participa en el torneo.

#### ⚙️ 4. **Configuración de Filtros**

La opción `list_filter` agrega filtros en la barra lateral de la vista de lista. En este caso, se incluye un filtro por:

- **Torneo**: Permite filtrar por el torneo asociado al equipo.

#### 🛠️ 5. **Método de Guardado Personalizado**

El método `save_model` es una función personalizada que se ejecuta cuando se guarda una instancia del modelo `TournamentTeam` desde el panel de administración. La función realiza una validación para evitar duplicados.

##### Validación:
- Antes de guardar, se verifica si ya existe una relación entre el mismo **torneo** (`tournament`) y el mismo **equipo** (`team`) en la base de datos.
- Si la relación ya existe, se lanza una **ValidationError** para evitar que se guarde la instancia y se notifica al usuario con el mensaje **"Este equipo ya está inscrito en este torneo."**

##### Parámetros:
- **request**: Objeto `HttpRequest` que representa la solicitud actual.
- **obj**: La instancia del modelo que se está guardando.
- **form**: El formulario de Django que contiene los datos del modelo.
- **change**: Booleano que indica si se está cambiando una instancia existente (`True`) o creando una nueva (`False`).

##### Comportamiento:
- Si no se encuentra un equipo inscrito previamente en el torneo, se guarda correctamente.
- Si el equipo ya está inscrito en el torneo, se genera una excepción para evitar el duplicado.

```python
# Configuración del administrador para el modelo TournamentTeam
@admin.register(TournamentTeam)
class TournamentTeamAdmin(admin.ModelAdmin):
    """Configuración del panel de administración para el modelo TournamentTeam.
    
    Personaliza la visualización de las relaciones Torneo-Equipo en el admin.
    """
    
    list_display = (
        'tournament',  # Nombre del torneo
        'team'        # Nombre del equipo
    )
    
    search_fields = (
        'tournament__name',  # Búsqueda por nombre de torneo
        'team__name'         # Búsqueda por nombre de equipo
    )
    
    list_filter = (
        'tournament',  # Filtro por torneo
    )

    def save_model(self, request, obj, form, change):
    """
    Guarda una instancia del modelo TournamentTeam desde el panel de administración.

    Validación:
    - Antes de guardar, verifica si ya existe una relación entre el mismo torneo (`tournament`)
      y equipo (`team`) en la base de datos.
    - Si ya existe, lanza una ValidationError para evitar duplicados y notificar al usuario.

    Parámetros:
    - request: Objeto HttpRequest que representa la solicitud actual.
    - obj: La instancia del modelo que se está guardando.
    - form: El formulario de Django que contiene los datos del modelo.
    - change: Booleano que indica si se está cambiando una instancia existente (True) o creando una nueva (False).
    """
    if TournamentTeam.objects.filter(tournament=obj.tournament, team=obj.team).exists():
        raise ValidationError("Este equipo ya está inscrito en este torneo.")
    super().save_model(request, obj, form, change)

```
---
### ⚽🎮 Configuración del Administrador para el Modelo `Match` 

Este archivo explica cómo configurar el panel de administración de Django para el modelo `Match`. La configuración personalizada se encuentra en la clase `MatchAdmin`, que permite personalizar la visualización y gestión de los partidos en el admin.

#### 📜 1. **Registro del Modelo en el Admin**

La clase `MatchAdmin` se registra con el decorador `@admin.register(Match)`. Esto indica que `MatchAdmin` se utilizará para configurar cómo se muestra el modelo `Match` en el panel de administración de Django.

#### 🗂️ 2. **Configuración de la Visualización de la Lista**

La opción `list_display` se usa para personalizar las columnas que se mostrarán en la lista de objetos dentro del admin. En este caso, se muestran los siguientes campos:

- 🏆 **Torneo**: Muestra el torneo asociado al partido.
- 🔢 **Ronda**: Indica la ronda del torneo en la que se está jugando el partido.
- 🎮 **Equipo 1**: Muestra el primer equipo que participa en el partido.
- 🎮 **Equipo 2**: Muestra el segundo equipo que participa en el partido.
- 📅 **Fecha Programada**: Muestra la fecha y hora programada para el partido.
- 📊 **Estado**: Muestra el estado actual del partido (pendiente, en progreso, finalizado, etc.).
- ✅ **Preparación del Equipo 1**: Muestra si el primer equipo está listo para el partido.
- ✅ **Preparación del Equipo 2**: Muestra si el segundo equipo está listo para el partido.
- ✔️ **Confirmación del Equipo 1**: Indica si el primer equipo ha confirmado su participación.
- ✔️ **Confirmación del Equipo 2**: Indica si el segundo equipo ha confirmado su participación.
- 🏆 **Ganador del Equipo 1**: Indica si el equipo 1 se ha autodeclarado ganador.
- 🏆 **Ganador del Equipo 2**: Indica si el equipo 2 se ha autodeclarado ganador.

#### 🔍 3. **Configuración de la Búsqueda**

La opción `search_fields` permite definir qué campos serán utilizados para realizar búsquedas dentro del admin. En este caso, se puede buscar por:

- **Nombre del torneo** al que pertenece el partido.
- **Nombre del equipo 1**.
- **Nombre del equipo 2**.

#### ⚙️ 4. **Configuración de Filtros**

La opción `list_filter` agrega filtros en la barra lateral de la vista de lista. En este caso, se incluyen los siguientes filtros:

- **Estado del partido**: Permite filtrar los partidos según su estado (pendiente, en progreso, finalizado, etc.).
- **Torneo**: Permite filtrar por el torneo al que pertenece el partido.

```python
# Configuración del administrador para el modelo Match
@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    """Configuración del panel de administración para el modelo Match.
    
    Personaliza la visualización y gestión de partidos en el admin de Django.
    """
    
    list_display = (
        'tournament',       # Torneo asociado
        'round',            # Ronda del torneo
        'team1',            # Primer equipo
        'team2',            # Segundo equipo
        'scheduled_at',     # Fecha programada
        'status',           # Estado del partido
        'team1_ready',      # Preparación equipo 1
        'team2_ready',      # Preparación equipo 2
        'team1_confirmed',  # Confirmación equipo 1
        'team2_confirmed',  # Confirmación equipo 2
        'team1_winner',     # Autodeclaración ganador equipo 1
        'team2_winner'      # Autodeclaración ganador equipo 2
    )
    
    search_fields = (
        'tournament__name',  # Búsqueda por nombre de torneo
        'team1__name',       # Búsqueda por nombre de equipo 1
        'team2__name'        # Búsqueda por nombre de equipo 2
    )
    
    list_filter = (
        'status',       # Filtro por estado del partido
        'tournament'    # Filtro por torneo
    )
```
---
### 🏆 Configuración del Administrador para el Modelo `MatchResult` 

Este archivo explica cómo configurar el panel de administración de Django para el modelo `MatchResult`. La configuración personalizada se encuentra en la clase `MatchResultAdmin`, que permite gestionar los resultados de los partidos en el admin.

#### 📜 1. **Registro del Modelo en el Admin**

La clase `MatchResultAdmin` se registra con el decorador `@admin.register(MatchResult)`. Esto indica que `MatchResultAdmin` se utilizará para configurar cómo se muestra el modelo `MatchResult` en el panel de administración de Django.

#### 🗂️ 2. **Configuración de la Visualización de la Lista**

La opción `list_display` se usa para personalizar las columnas que se mostrarán en la lista de objetos dentro del admin. En este caso, se muestran los siguientes campos:

- ⚽ **Partido**: Muestra el partido asociado al resultado.
- 🏆 **Equipo Ganador**: Muestra el equipo que ganó el partido.
- 🏅 **Puntuación del Equipo 1**: Muestra la puntuación obtenida por el primer equipo.
- 🏅 **Puntuación del Equipo 2**: Muestra la puntuación obtenida por el segundo equipo.
- 📅 **Fecha de Finalización**: Muestra la fecha en que se completó el partido.

#### 🔍 3. **Configuración de la Búsqueda**

La opción `search_fields` permite definir qué campos serán utilizados para realizar búsquedas dentro del admin. En este caso, se puede buscar por:

- **Nombre del equipo 1** en el partido.
- **Nombre del equipo 2** en el partido.

#### ⚙️ 4. **Configuración de Filtros**

La opción `list_filter` agrega filtros en la barra lateral de la vista de lista. En este caso, se incluye el siguiente filtro:

- **Fecha de finalización**: Permite filtrar los resultados de los partidos por la fecha en que se completaron.

```python
# Configuración del administrador para el modelo MatchResult
@admin.register(MatchResult)
class MatchResultAdmin(admin.ModelAdmin):
    """Configuración del panel de administración para el modelo MatchResult.
    
    Personaliza la visualización de los resultados de partidos en el admin.
    """
    
    list_display = (
        'match',         # Partido asociado
        'winner',        # Equipo ganador
        'team1_score',   # Puntuación equipo 1
        'team2_score',   # Puntuación equipo 2
        'completed_at'   # Fecha de finalización
    )
    
    search_fields = (
        'match__team1__name',  # Búsqueda por nombre de equipo 1
        'match__team2__name'   # Búsqueda por nombre de equipo 2
    )
    
    list_filter = (
        'completed_at',  # Filtro por fecha de finalización
    )
```
---
### 📝 Configuración del Administrador para el Modelo `MatchLog` 

Este archivo explica cómo configurar el panel de administración de Django para el modelo `MatchLog`. La configuración personalizada se encuentra en la clase `MatchLogAdmin`, que permite gestionar los registros de eventos de los partidos.

#### 📜 1. **Registro del Modelo en el Admin**

La clase `MatchLogAdmin` se registra con el decorador `@admin.register(MatchLog)`. Esto indica que `MatchLogAdmin` se utilizará para configurar cómo se muestra el modelo `MatchLog` en el panel de administración de Django.

#### 🗂️ 2. **Configuración de la Visualización de la Lista**

La opción `list_display` se usa para personalizar las columnas que se mostrarán en la lista de objetos dentro del admin. En este caso, se muestran los siguientes campos:

- ⚽ **Partido**: Muestra el partido al que pertenece el registro del evento.
- 🏅 **Equipo**: Muestra el equipo involucrado en el evento (opcional).
- 👤 **Jugador**: Muestra el jugador involucrado en el evento (opcional).
- 📝 **Evento**: Muestra la descripción del evento (ej: gol, tarjeta, etc.).
- 📅 **Fecha del Registro**: Muestra la fecha en que se registró el evento.

#### 🔍 3. **Configuración de la Búsqueda**

La opción `search_fields` permite definir qué campos serán utilizados para realizar búsquedas dentro del admin. En este caso, se puede buscar por:

- **Nombre del equipo 1** o **equipo 2** en el partido.
- **Nombre de usuario del jugador** involucrado en el evento.

#### ⚙️ 4. **Configuración de Filtros**

La opción `list_filter` agrega filtros en la barra lateral de la vista de lista. En este caso, se incluye el siguiente filtro:

- **Fecha de creación**: Permite filtrar los registros de los eventos por la fecha en que se crearon.

```python
# Configuración del administrador para el modelo MatchLog
@admin.register(MatchLog)
class MatchLogAdmin(admin.ModelAdmin):
    """Configuración del panel de administración para el modelo MatchLog.
    
    Personaliza la visualización de los registros de eventos de partidos en el admin.
    """
    
    list_display = (
        'match',        # Partido relacionado
        'team',         # Equipo involucrado (opcional)
        'player',       # Jugador involucrado (opcional)
        'event',        # Descripción del evento
        'created_at'    # Fecha del registro
    )
    
    search_fields = (
        'match__team1__name',     # Búsqueda por nombre de equipo 1 del partido
        'match__team2__name',     # Búsqueda por nombre de equipo 2 del partido
        'player__user__username'  # Búsqueda por nombre de usuario del jugador
    )
    
    list_filter = (
        'created_at',  # Filtro por fecha de creación del registro
    )
```
---
### 🎁 Configuración del Administrador para el Modelo `Reward` 

Este archivo explica cómo configurar el panel de administración de Django para el modelo `Reward`. La configuración personalizada se encuentra en la clase `RewardAdmin`, que permite gestionar las recompensas dentro del sistema.

#### 📜 1. **Registro del Modelo en el Admin**

La clase `RewardAdmin` se registra con el decorador `@admin.register(Reward)`. Esto indica que `RewardAdmin` se utilizará para personalizar la visualización y comportamiento del modelo `Reward` en el panel de administración de Django.

#### 🗂️ 2. **Configuración de la Visualización de la Lista**

La opción `list_display` se usa para personalizar las columnas que se mostrarán en la lista de objetos dentro del admin. En este caso, se muestran los siguientes campos:

- 🎁 **Nombre de la recompensa**: Muestra el nombre de la recompensa.
- 💰 **Costo en monedas**: Muestra el costo en monedas de la recompensa.
- 📦 **Stock**: Muestra la cantidad disponible de la recompensa.
- ✅ **Estado activo/inactivo**: Muestra si la recompensa está activa o no.
- 🖼️ **Vista previa de la imagen**: Muestra una miniatura de la imagen asociada a la recompensa.
- 📅 **Fecha de creación**: Muestra la fecha en la que se creó la recompensa.

#### 🔍 3. **Configuración de la Búsqueda**

La opción `search_fields` permite definir qué campos serán utilizados para realizar búsquedas dentro del admin. En este caso, se puede buscar por:

- **Nombre de la recompensa**.

#### ⚙️ 4. **Configuración de Filtros**

La opción `list_filter` agrega filtros en la barra lateral de la vista de lista. En este caso, se incluye el siguiente filtro:

- **Estado activo/inactivo**: Permite filtrar las recompensas según su estado (activo o inactivo).

#### 🖼️ 5. **Método de Vista Previa de la Imagen**

La función **vista previa de imagen** genera una miniatura de la imagen de la recompensa para mostrarla en el panel de administración. Si la recompensa tiene una imagen asociada, se presenta una pequeña vista previa de la imagen. Si no hay imagen disponible, se muestra el texto **"No image"**.

##### Comportamiento:
- Si la recompensa tiene una imagen, se muestra una miniatura de 50x50 píxeles con bordes redondeados.
- Si no hay imagen, se muestra el mensaje **"No image"**.

##### Descripción de la columna:
El nombre de la columna en el panel de administración es **"Image Preview"**.

```python
# Configuración del administrador para el modelo Reward
@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    """Configuración del panel de administración para el modelo Reward.
    
    Personaliza cómo se muestran y gestionan las recompensas en el admin de Django.
    """
    
    list_display = (
        'name',          # Nombre de la recompensa
        'coins_cost',    # Costo en monedas
        'stock',         # Cantidad disponible
        'is_active',     # Estado activo/inactivo
        'image_preview', # Vista previa de la imagen
        'created_at'     # Fecha de creación
    )
    
    search_fields = (
        'name',  # Búsqueda por nombre de recompensa
    )
    
    list_filter = (
        'is_active',  # Filtro por estado activo/inactivo
    )

    def image_preview(self, obj):
        """Genera una miniatura de la imagen de la recompensa.
        
        Args:
            obj: Instancia del modelo Reward
            
        Returns:
            HTML con la imagen en miniatura o texto si no existe imagen
        """
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 5px;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = "Image Preview"  # Nombre de la columna

```
---

### 🔄 Configuración del Administrador para el Modelo `Redemption` 

Este archivo explica cómo configurar el panel de administración de Django para el modelo `Redemption`. La configuración personalizada se encuentra en la clase `RedemptionAdmin`, que permite gestionar los canjes de recompensas dentro del sistema.

#### 📜 1. **Registro del Modelo en el Admin**

La clase `RedemptionAdmin` se registra con el decorador `@admin.register(Redemption)`. Esto indica que `RedemptionAdmin` se utilizará para personalizar la visualización y el comportamiento del modelo `Redemption` en el panel de administración de Django.

#### 🗂️ 2. **Configuración de la Visualización de la Lista**

La opción `list_display` se usa para personalizar las columnas que se mostrarán en la lista de objetos dentro del admin. En este caso, se muestran los siguientes campos:

- 👤 **Usuario**: Muestra el usuario que realizó el canje de la recompensa.
- 🎁 **Recompensa canjeada**: Muestra la recompensa que fue canjeada.
- 📅 **Fecha del canje**: Muestra la fecha en la que se realizó el canje.

#### 🔍 3. **Configuración de la Búsqueda**

La opción `search_fields` permite definir qué campos serán utilizados para realizar búsquedas dentro del admin. En este caso, se puede buscar por:

- **Nombre de usuario** del usuario que realizó el canje.
- **Nombre de la recompensa** que fue canjeada.

#### ⚙️ 4. **Configuración de Filtros**

La opción `list_filter` agrega filtros en la barra lateral de la vista de lista. En este caso, se incluye el siguiente filtro:

- **Fecha del canje**: Permite filtrar los canjes por la fecha en que fueron realizados.

```python
# Configuración del administrador para el modelo Redemption
@admin.register(Redemption)
class RedemptionAdmin(admin.ModelAdmin):
    """Configuración del panel de administración para el modelo Redemption.
    
    Personaliza la visualización de los canjes de recompensas en el admin.
    """
    
    list_display = (
        'user',         # Usuario que realizó el canje
        'reward',       # Recompensa canjeada
        'redeemed_at'   # Fecha del canje
    )
    
    search_fields = (
        'user__username',  # Búsqueda por nombre de usuario
        'reward__name'     # Búsqueda por nombre de recompensa
    )
    
    list_filter = (
        'redeemed_at',  # Filtro por fecha de canje
    )
```
---

## 🔄 Navegación
[⬅️ Volver al README principal](../README.md)

## 🔄 Navegación
[⬅️ Volver al README principal](../README.md)
