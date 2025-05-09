#  📜 Explicación de algunas vistas importantes en Django (`views.py`)

Este archivo define algunas de las vistas más importantes de la aplicación web. Las vistas son componentes esenciales en Django, ya que manejan la lógica detrás de las solicitudes HTTP y devuelven las respuestas correspondientes. A continuación, se describen las vistas:

---

## 🏆 Explicación de la vista `TournamentListAPI` en Django

En esta sección explicamos la vista `TournamentListAPI`, que se encarga de devolver una lista de torneos a través de la API utilizando Django Rest Framework (DRF).

### 🌍 ¿Qué es una vista `ListAPIView`?

La vista `ListAPIView` es una vista basada en clases de Django Rest Framework (DRF) que se utiliza para devolver una lista de objetos de un modelo. Es ideal para mostrar colecciones de datos en una API. A diferencia de las vistas basadas en funciones, las vistas basadas en clases permiten una mayor organización y reutilización del código.

### 🛠️ Desglose de la vista `TournamentListAPI`

- **`queryset`**: Este es el conjunto de objetos que nuestra vista va a devolver. En este caso, estamos obteniendo todos los objetos de la base de datos que pertenecen al modelo `Tournament`. Básicamente, estamos consultando todos los torneos que existen en la base de datos.
  
- **`serializer_class`**: Aquí especificamos qué serializador se debe usar para convertir los objetos de tipo `Tournament` en datos JSON. El serializador es responsable de transformar los datos del modelo en un formato adecuado para la respuesta de la API. Este serializador se utiliza para definir qué campos de los torneos se deben devolver y cómo deben representarse.

### 🧠 Optimización del QuerySet

Incluye una versión personalizada del conjunto de datos (queryset) con las siguientes optimizaciones:

- 🔗 **`select_related('created_by')`**: Precarga la información del usuario que creó el torneo, reduciendo consultas adicionales a la base de datos.
- 📦 **`prefetch_related('teams', 'matches')`**: Precarga las relaciones con equipos participantes y partidos del torneo, mejorando el rendimiento al evitar consultas repetidas.

### 🔄 ¿Cómo funciona esta vista?

1. **Solicitud GET**: Cuando se realiza una solicitud HTTP GET a la URL asociada con esta vista, Django Rest Framework ejecuta la lógica definida en `TournamentListAPI`.
2. **Consulta a la base de datos**: La vista consulta la base de datos y obtiene todos los objetos del modelo `Tournament`.
3. **Transformación en JSON**: El serializador convierte los datos de cada objeto `Tournament` a un formato JSON adecuado.
4. **Respuesta al cliente**: Finalmente, la vista devuelve esta respuesta al cliente en formato JSON, que contiene los detalles de todos los torneos en la base de datos.

### 📊 Resultado

La respuesta será una lista de objetos JSON, donde cada objeto representará un torneo y contendrá los campos relevantes como el nombre del torneo, el juego asociado, el estado, la fecha de inicio, el número máximo de equipos, entre otros.

### 🎯 Beneficios de usar `ListAPIView`

- **Código limpio y reutilizable**: Al usar vistas genéricas, no necesitas escribir mucha lógica repetitiva. Solo necesitas especificar el conjunto de datos y el serializador, y Django Rest Framework se encarga del resto.
- **Respuesta automática en formato JSON**: DRF convierte automáticamente los objetos de Django en formato JSON, lo que simplifica la implementación.
- **Configuración rápida y sencilla**: Solo tienes que definir qué modelo y qué serializador utilizar, y la vista ya está lista para usar.

```python
class TournamentListAPI(generics.ListAPIView):
    """
    API endpoint que permite listar todos los torneos disponibles en el sistema.
    
    Proporciona una interfaz de solo lectura (GET) para acceder a la información
    básica de los torneos. Utiliza el serializer TournamentSerializer para definir
    la estructura de los datos devueltos.

    Atributos:
        queryset (QuerySet): Todos los objetos Tournament existentes
        serializer_class (Serializer): Clase que controla la serialización a JSON

    Métodos heredados:
        get: Maneja las solicitudes GET y devuelve la lista de jugadores serializados.
    """
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

    def get_queryset(self):
            """
            Versión optimizada del queryset que incluye prefetch de relaciones comunes.
            
            Returns:
                QuerySet: Torneos con sus relaciones precargadas para mejor performance
            """
            return super().get_queryset().select_related('created_by').prefetch_related('teams', 'matches')
```
---

## 🏅 Explicación de la vista `PlayerStatsListAPI` en Django

En esta sección, vamos a explicar la vista `PlayerStatsListAPI`, que se encarga de devolver una lista de jugadores junto con sus estadísticas a través de una API utilizando Django Rest Framework (DRF).

### 🌍 ¿Qué es una vista `ListAPIView`?

La vista `ListAPIView` es una vista genérica proporcionada por Django Rest Framework que se utiliza para devolver una lista de objetos de un modelo específico. Es especialmente útil cuando queremos mostrar un conjunto de datos completos en formato JSON, como una lista de jugadores en una base de datos.

### 🛠️ Desglose de la vista `PlayerStatsListAPI`

- **`queryset`**: Este es el conjunto de objetos que la vista va a devolver. En este caso, estamos consultando todos los objetos del modelo `Player`, lo que significa que la vista devolverá todos los jugadores de la base de datos.
  
- **`serializer_class`**: Aquí definimos el serializador que se usará para convertir los objetos del modelo `Player` en formato JSON. El serializador convierte las instancias del modelo `Player` en un formato adecuado para ser enviado como respuesta en la API.

### 🧠 Optimización del QuerySet

Incluye una versión personalizada del conjunto de datos (queryset) con las siguientes optimizaciones:

- 🔗 **`select_related('created_by')`**: Precarga la información del usuario que creó el torneo, reduciendo consultas adicionales a la base de datos.
- 📦 **`prefetch_related('teams', 'matches')`**: Precarga las relaciones con equipos participantes y partidos del torneo, mejorando el rendimiento al evitar consultas repetidas.

### 🔄 ¿Cómo funciona esta vista?

1. **Solicitud GET**: Cuando se realiza una solicitud HTTP GET a la URL asociada con esta vista, Django Rest Framework ejecuta la lógica definida en `PlayerStatsListAPI`.
2. **Consulta a la base de datos**: La vista consulta la base de datos y obtiene todos los objetos del modelo `Player`.
3. **Transformación en JSON**: El serializador convierte los datos de cada objeto `Player` a un formato JSON adecuado.
4. **Respuesta al cliente**: Finalmente, la vista devuelve esta respuesta al cliente en formato JSON, que contiene los detalles de todos los jugadores junto con sus estadísticas.

### 📊 Resultado

La respuesta será una lista de objetos JSON, donde cada objeto representará a un jugador y contendrá los campos relevantes como su nombre de usuario, equipo, estadísticas de partidas jugadas, ganadas, el rol, el país, entre otros.

### 🎯 Beneficios de usar `ListAPIView`

- **Simplicidad**: Usar `ListAPIView` permite definir una vista de lista de forma rápida y sin necesidad de escribir lógica adicional.
- **Automatización del formato JSON**: DRF se encarga de convertir los objetos del modelo a formato JSON automáticamente, lo que facilita la integración de la API.
- **Facilidad de mantenimiento**: La vista está construida de manera que es fácil de extender o modificar en el futuro si es necesario.

```python
class PlayerStatsListAPI(generics.ListAPIView):
    """
    API endpoint que permite ver las estadísticas de todos los jugadores en formato JSON.
    
    Hereda de ListAPIView para proporcionar un endpoint de solo lectura (GET).
    Utiliza PlayerStatsSerializer para convertir los objetos Player a formato JSON.

    Atributos:
        queryset (QuerySet): Todos los objetos Player existentes en la base de datos.
        serializer_class (Serializer): Clase serializadora que define la representación JSON.

    Métodos heredados de ListAPIView:
        get: Maneja las solicitudes GET y devuelve la lista de jugadores serializados.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerStatsSerializer

    def get_queryset(self):
        """
        Opcional: Sobrescribe el queryset base para agregar filtros o optimizaciones.
        
        Returns:
            QuerySet: Conjunto de jugadores potencialmente filtrado/optimizado.
        """
        return super().get_queryset().select_related('team')
```
---

# 🏠 Vista `IndexView` en Django

La vista `IndexView` es una vista basada en clases que se encarga de mostrar la página principal del sitio web una vez que el usuario ha iniciado sesión. Utiliza `TemplateView` de Django junto con el mixin `LoginRequiredMixin`.

### 🔐 Requiere Autenticación

Gracias al uso de `LoginRequiredMixin`, esta vista solo estará disponible para usuarios autenticados. Si un usuario no ha iniciado sesión, será redirigido automáticamente a la página de login.

### 🧩 Template asociado

- **`template_name`**: Se especifica que esta vista utilizará el archivo `web/index.html` como plantilla para renderizar la página.

### 📦 Contexto adicional

Dentro del método `get_context_data`, se agrega un nuevo dato al contexto:

- **`game_list`**: Una lista con todos los objetos del modelo `Game`, que estará disponible dentro de la plantilla HTML para ser utilizada, por ejemplo, en una tabla o en una lista de juegos.

### 🎯 ¿Qué logra esta vista?

- Restringe el acceso solo a usuarios registrados ✅  
- Carga la página principal (`index.html`) 🖥️  
- Proporciona a la plantilla una lista completa de juegos para su visualización 🕹️  

```python
class IndexView(LoginRequiredMixin, TemplateView):
    """
    Vista principal que muestra la página de inicio de la aplicación.
    
    Requiere que el usuario esté autenticado (heredando de LoginRequiredMixin)
    y muestra una lista de todos los juegos disponibles en el sistema.

    Atributos:
        template_name (str): Ruta al template HTML que renderiza la vista.

    Métodos:
        get_context_data(**kwargs): Añade la lista de juegos al contexto de renderizado.
    """
    template_name = 'web/index.html'

    def get_context_data(self, **kwargs):
        """
        Añade datos adicionales al contexto de la vista.

        Args:
            **kwargs: Argumentos clave adicionales.

        Returns:
            dict: Contexto enriquecido con la lista de todos los juegos.
        """
        context = super().get_context_data(**kwargs)
        context['game_list'] = Game.objects.all()
        return context
```
---
## 🧑‍🤝‍🧑 Vista `MyTournamentListView` – Torneos del Jugador Actual

Esta vista basada en clase (`ListView`) muestra una lista personalizada de torneos en los que participa el equipo del **jugador actualmente autenticado**.

### 🔐 Requiere Autenticación

Gracias al uso de `LoginRequiredMixin`, solo los usuarios autenticados pueden acceder a esta vista. Si un visitante no ha iniciado sesión, será redirigido a la página de login.

### 🎯 ¿Qué muestra?

Muestra únicamente los **torneos donde participa el equipo del jugador actual**. Si el jugador no tiene equipo asignado, no se mostrarán torneos.

### ⚙️ Comportamiento del QuerySet

- Se busca al usuario a través del ID (`pk`) pasado por URL.
- Luego se obtiene el objeto `Player` relacionado con ese usuario.
- Si ese jugador tiene un equipo asociado, se filtran todos los torneos donde ese equipo esté inscrito.
- Si no tiene equipo o no es un jugador válido, se devuelve una lista vacía.

### 🧾 Detalles técnicos

- 🧱 Modelo: `Tournament`
- 📄 Template: `web/my_tournament_list.html`
- 📦 Contexto: La lista se accede mediante la variable `tournament_list` en el template.

```python
class MyTournamentListView(LoginRequiredMixin, ListView):
    """
    Vista que muestra la lista de torneos en los que participa el equipo del jugador actual.
    
    Requiere autenticación y muestra solo los torneos donde el equipo del jugador
    está registrado. Si el jugador no tiene equipo asociado, devuelve una lista vacía.

    Atributos:
        model (Model): Modelo Tournament utilizado para la consulta
        template_name (str): Ruta al template que renderiza la vista
        context_object_name (str): Nombre de la variable de contexto para la lista

    Métodos:
        get_queryset: Filtra los torneos donde participa el equipo del jugador
    """
    model = Tournament
    template_name = 'web/my_tournament_list.html'
    context_object_name = 'tournament_list'

    def get_queryset(self):
        """
        Obtiene los torneos asociados al equipo del jugador actual.
        
        Returns:
            QuerySet: Torneos donde participa el equipo del jugador o queryset vacío si:
                     - El usuario no existe
                     - No tiene jugador asociado
                     - El jugador no tiene equipo
        """
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        player = Player.objects.filter(user=user).first()

        if player and player.team:
            return Tournament.objects.filter(
                tournamentteam__team=player.team
            ).distinct()
        return Tournament.objects.none()
```
---
## 🏆 Vista `TournamentDetailView` – Detalles del Torneo

Muestra toda la información relevante sobre un **torneo específico**, incluyendo si el usuario actual está registrado a través de su equipo. Ideal para acceder desde un listado o tarjeta de torneos.

### 🔐 Requiere Autenticación

Utiliza `LoginRequiredMixin` para asegurar que **solo usuarios autenticados** puedan acceder a los detalles. Si no estás logueado, se redirige al formulario de inicio de sesión.

### 🔎 ¿Qué muestra?

- 📌 Información detallada del torneo:
  - Nombre, juego, fechas, estado, descripción, etc.
- ✅ Estado de registro del usuario actual (si participa a través de su equipo).
- 👥 Listado de equipos inscritos con sus respectivos jugadores y usuarios.

### 🧠 Lógica del Contexto

El método `get_context_data()` extiende el contexto con:

| Variable             | Tipo     | Descripción                                                                 |
|----------------------|----------|-----------------------------------------------------------------------------|
| `tournament`         | `object` | Objeto principal del torneo                                                 |
| `is_registered`      | `bool`   | `True` si el jugador del usuario está en un equipo inscrito en este torneo |
| `player`             | `Player` | Instancia del jugador autenticado (si existe)                              |
| `tournament_teams`   | `QuerySet` | Lista optimizada de equipos inscritos, con sus jugadores y usuarios        |

Esto permite en el template:

- Mostrar un mensaje como **"Ya estás registrado en este torneo"** ✅
- Ocultar o mostrar botones como "Unirse al torneo" ❌
- Renderizar la lista de equipos participantes 👥

### ⚙️ Optimización

La vista usa `select_related` y `prefetch_related` para evitar **consultas innecesarias** en la base de datos:

- `Player` se trae junto a `User` y su `Team`
- Los equipos del torneo traen sus jugadores y los usuarios asociados

### 🧾 Detalles Técnicos

- 🧱 Modelo base: `Tournament`
- 📄 Template: `web/tournament_detail.html`
- 🔁 Vista: `DetailView` con contexto extendido

```python
class TournamentDetailView(LoginRequiredMixin, DetailView):
    """
    Vista que muestra los detalles de un torneo específico.

    Requiere autenticación (LoginRequiredMixin) y muestra información detallada
    de un torneo individual, incluyendo el estado de registro del usuario actual.

    Atributos:
        model (Model): Modelo Tournament que contiene los datos del torneo
        template_name (str): Ruta al template que renderiza la vista (web/tournament_detail.html)
        context_object_name (str): Nombre de la variable que contendrá el objeto Tournament en el contexto del template

    Métodos heredados de DetailView:
        get_object: Obtiene el objeto Tournament basado en los parámetros de la URL
        get_context_data: Proporciona el contexto para renderizar el template
    """
    model = Tournament
    template_name = 'web/tournament_detail.html'
    context_object_name = 'tournament'

    def get_context_data(self, **kwargs):
        """
        Extiende el contexto base con información sobre si el usuario actual
        está registrado en el torneo.

        Returns:
            dict: Contexto que incluye:
                - is_registered: Booleano indicando si el usuario está registrado en el torneo
                - player: Objeto player con los datos del jugador
                - tournament_teams: Lista de objetos tournamentTeams con los datos de los equipos que participan en el torneo
        """
        context = super().get_context_data(**kwargs)
        tournament = context['tournament']
        user = self.request.user

        is_registered = False
        player = None

        if user.is_authenticated:
            try:
                player = Player.objects.select_related('team').get(user=user)
                is_registered = TournamentTeam.objects.filter(
                    tournament=tournament,
                    team__player=player
                ).exists()
            except Player.DoesNotExist:
                is_registered = False

        # Pre-cargar equipos del torneo con sus jugadores y usuarios
        tournament_teams = TournamentTeam.objects.filter(tournament=tournament).select_related(
            'team'
        ).prefetch_related(
        Prefetch('team__player_set', queryset=Player.objects.select_related('user'))
    )

        context['is_registered'] = is_registered
        context['player'] = player
        context['tournament_teams'] = tournament_teams

        return context
```
## 🛠️ Vista `TeamCreateInTournamentView` – Crear Equipo en un Torneo

Esta vista permite a un jugador crear un nuevo equipo **directamente dentro de un torneo específico**. Se utiliza cuando el jugador desea participar en un torneo pero aún no tiene equipo.

### 🔐 Requiere Autenticación

Como hereda de `LoginRequiredMixin`, solo los usuarios autenticados pueden acceder a esta funcionalidad.

### 🧱 Tipo de vista

Basada en `CreateView`, está diseñada para gestionar formularios de creación de objetos. En este caso, un nuevo equipo (`Team`).

### 📋 ¿Qué hace?

1. **Obtiene el torneo** al que se asociará el nuevo equipo (a través de `pk` en la URL).
2. **Crea el equipo** a partir del formulario enviado.
3. **Asocia ese equipo con el torneo** creando una entrada en `TournamentTeam`.
4. **Asigna el jugador autenticado** como líder del equipo recién creado.
5. **Habilita la búsqueda de compañeros**, si el torneo permite más de un jugador por equipo.
6. **Redirige al usuario** a la lista de equipos del torneo.

### ⚙️ Contexto y funcionalidad clave

- 🔄 Redirección final: vista de equipos para ese torneo.
- 👤 El jugador que crea el equipo se convierte automáticamente en el líder del equipo.
- 🧑‍🤝‍🧑 Si el torneo permite múltiples miembros por equipo, el nuevo equipo se marca como "buscando compañeros".

### 🧾 Detalles técnicos

- 🧱 Modelo: `Team`
- 📄 Template: `web/team_create_in_tournament.html`
- 📝 Formulario: `TeamForm`
- 🔄 Redirección: `tournamentDetailView` con el pk del torneo


```python
class TeamCreateInTournamentView(LoginRequiredMixin, CreateView):
    """
    Vista para crear un nuevo equipo dentro de un torneo específico.

    Requiere autenticación (LoginRequiredMixin) y permite a un usuario crear
    un equipo que será automáticamente asociado al torneo especificado.

    Atributos:
        model (Model): Modelo Team utilizado para la creación
        template_name (str): Ruta al template del formulario de creación
        form_class (Form): Clase del formulario para crear equipos

    Métodos:
        dispatch: Obtiene el torneo asociado antes de procesar la solicitud
        form_valid: Procesa el formulario válido creando las relaciones necesarias
        get_context_data: Añade el torneo al contexto del template
    """
    model = Team
    template_name = 'web/team_create_in_tournament.html'
    form_class = TeamForm

    def dispatch(self, request, *args, **kwargs):
        """
        Prepara la vista obteniendo el torneo asociado antes de procesar la solicitud.

        Args:
            request: Objeto HttpRequest
            *args: Argumentos variables
            **kwargs: Argumentos clave variables

        Returns:
            HttpResponse: Respuesta del método dispatch de la superclase
        """
        self.tournament = get_object_or_404(Tournament, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Procesa un formulario válido realizando:
        1. Creación del equipo
        2. Asociación con el torneo
        3. Asignación del jugador como miembro y líder
        4. Redirección a la vista de equipos del torneo

        Args:
            form (Form): Formulario de creación de equipo validado

        Returns:
            HttpResponseRedirect: Redirección a la vista de equipos del torneo
        """
        team = form.save()
        TournamentTeam.objects.create(tournament=self.tournament, team=team)
        
        player = Player.objects.filter(user=self.request.user).first()
        if player:
            player.team = team
            team.leader = player
            if self.tournament.max_player_per_team > 1:
                team.searching_teammates = True
            player.save()
            team.save()

        return redirect('web:tournamentDetailView', pk=self.tournament.pk)

    def get_context_data(self, **kwargs):
        """
        Añade el torneo al contexto del template.

        Args:
            **kwargs: Argumentos clave adicionales

        Returns:
            dict: Contexto enriquecido con el objeto Tournament
        """
        context = super().get_context_data(**kwargs)
        context['tournament'] = self.tournament
        return context
```
---

## 🆕 Vista `TeamCreateView` – Crear un Nuevo Equipo

Permite a un jugador autenticado **crear un nuevo equipo** desde cero. Ideal para jugadores que aún no están en un equipo y desean liderar uno.

### 🔐 Requiere Autenticación

Esta vista usa `LoginRequiredMixin`, por lo que solo los usuarios con sesión iniciada pueden acceder.

### 🧱 Tipo de Vista

Está basada en `CreateView`, lo que permite presentar un formulario para crear instancias del modelo `Team`.

### 📋 ¿Qué hace?

1. Muestra un formulario para crear un equipo.
2. Al enviarlo correctamente:
   - Guarda el nuevo equipo.
   - Asigna al usuario autenticado como **jugador líder** del equipo.
   - Vincula al jugador con el equipo creado.
3. Redirige al usuario a la vista de detalle de su equipo (`playerTeamDetailView`).

### ⚙️ Detalles Técnicos

- 🧱 **Modelo**: `Team`
- 📄 **Template**: `web/team_create.html`
- 📝 **Formulario**: `TeamForm`
- 🔁 **Redirección**: a la vista de detalle del jugador y su equipo

### 👤 Asignación Automática

El jugador que crea el equipo se convierte en su líder y queda asociado automáticamente al nuevo equipo. Esto simplifica la experiencia de usuario y garantiza una estructura clara desde el inicio.

```python
class TeamCreateView(LoginRequiredMixin, CreateView):
    """
    Vista para la creación de un nuevo equipo.

    Requiere autenticación (LoginRequiredMixin) y permite a un usuario crear
    un nuevo equipo, asignándose automáticamente como miembro y líder del mismo.

    Atributos:
        model (Model): Modelo Team utilizado para la creación
        template_name (str): Ruta al template del formulario de creación
        form_class (Form): Clase del formulario para crear equipos

    Métodos:
        form_valid: Procesa el formulario válido creando el equipo y asignando al usuario
    """
    model = Team
    template_name = 'web/team_create.html'
    form_class = TeamForm

    def form_valid(self, form):
        """
        Procesa un formulario válido realizando:
        1. Creación del equipo
        2. Asignación del jugador como miembro y líder
        3. Redirección a la vista de detalle del equipo

        Args:
            form (Form): Formulario de creación de equipo validado

        Returns:
            HttpResponseRedirect: Redirección a la vista de detalle del equipo del jugador
        """
        team = form.save()
        player = Player.objects.filter(user=self.request.user).first()
        if player:
            player.team = team
            team.leader = player
            player.save()
            team.save()

        return redirect('web:playerTeamDetailView', pk=player.id)
```
---
## 🗑️ Vista `TeamDeleteView` – Eliminar un Equipo

Permite a un usuario autenticado **eliminar su equipo**, con condiciones de seguridad que evitan la eliminación accidental o inapropiada.

### 🔐 Requiere Autenticación

Solo jugadores con sesión iniciada pueden intentar eliminar un equipo, gracias al uso de `LoginRequiredMixin`.

### 📋 ¿Qué hace?

1. 🔍 Verifica que el usuario sea el **líder del equipo**.
2. ❌ No permite eliminar equipos **registrados en torneos**.
3. ✅ Si se cumplen ambas condiciones:
   - El equipo es eliminado.
   - Se muestra un mensaje de éxito.
4. 🔄 Redirige al usuario a su vista de equipo.

### ⚠️ Validaciones Críticas

- **Permiso del líder**: Solo el jugador que lidera el equipo puede eliminarlo.
- **Participación en torneos**: Si el equipo está inscrito en al menos un torneo, no podrá eliminarse.

### 🛠️ Lógica detrás del POST

- Se obtiene el equipo por su `pk`.
- Se comprueba el usuario actual y su rol de líder.
- Se verifica si hay registros en `TournamentTeam`.
- Se elimina el equipo si todo está en orden.
- Se usan mensajes (`messages`) para dar retroalimentación al usuario.

```python
class TeamDeleteView(LoginRequiredMixin, View):
    """
    Vista para eliminar un equipo existente.

    Requiere autenticación (LoginRequiredMixin) y verifica que el usuario sea el líder
    del equipo y que el equipo no esté registrado en ningún torneo antes de permitir
    su eliminación.

    Métodos:
        post: Maneja la solicitud de eliminación con las validaciones correspondientes
    """
    def post(self, request, *args, **kwargs):
        """
        Procesa la solicitud de eliminación de equipo realizando:
        1. Verificación de permisos (solo el líder puede eliminar)
        2. Verificación de participación en torneos
        3. Eliminación del equipo si se cumplen las condiciones
        4. Redirección con mensajes de retroalimentación

        Args:
            request: Objeto HttpRequest
            *args: Argumentos variables
            **kwargs: Argumentos clave variables (incluye 'pk' del equipo)

        Returns:
            HttpResponseRedirect: Redirección a la vista de detalle del jugador
        """
        team = get_object_or_404(Team, pk=kwargs['pk'])

        if team.leader.user != request.user:
            messages.error(request, "No tienes permiso para eliminar este equipo.")
            return redirect('web:playerTeamDetailView', pk=request.user.player.pk)

        if TournamentTeam.objects.filter(team=team).exists():
            messages.error(request, "No se puede eliminar el equipo porque está inscrito en un torneo.")
            return redirect('web:playerTeamDetailView', pk=request.user.player.pk)

        team.delete()
        messages.success(request, "El equipo ha sido eliminado exitosamente.")
        return redirect('web:playerTeamDetailView', pk=request.user.player.pk)
```
---
## 🔄 Vista `ToggleSearchingTeammatesView` – Activar/Desactivar Búsqueda de Compañeros

Permite a un jugador **activar o desactivar la búsqueda de nuevos compañeros de equipo** para su equipo actual, siempre que se cumplan ciertas condiciones.

### 🔐 Requiere Autenticación y Rol de Líder

Solo jugadores autenticados que sean **líderes del equipo** pueden cambiar este estado.

### 🧠 ¿Qué hace esta vista?

1. ✅ Verifica que el usuario sea el líder del equipo.
2. 🛑 Impide activar la búsqueda si el equipo está en un **torneo en curso**.
3. 🧍‍♂️ Impide activar la búsqueda si el equipo ya está **completo en un torneo próximo**.
4. 🔄 Cambia el estado `searching_teammates` del equipo.
5. 📨 Muestra un mensaje de éxito o error según corresponda.
6. 🔁 Redirige al jugador a la vista de detalle de su equipo.

### 📌 Reglas Importantes

- 🚫 Si hay un torneo activo (`status='Ongoing'`), **no se puede buscar jugadores nuevos**.
- 📋 En torneos próximos (`status='Upcoming'`), **no se puede activar la búsqueda si el equipo ya tiene el máximo de jugadores**.

### 📎 Resultado Esperado

El botón de "Buscar compañeros" del equipo **activará o desactivará** esta opción según el contexto del torneo y la capacidad del equipo.

```python
class ToggleSearchingTeammatesView(LoginRequiredMixin, View):
    """
    Vista para activar/desactivar la búsqueda de compañeros de equipo.

    Requiere autenticación y permisos de líder del equipo para modificar
    el estado de búsqueda de jugadores. Incluye validaciones para evitar
    cambios no permitidos durante torneos activos o cuando el equipo está lleno.

    Métodos:
        post: Maneja la solicitud de cambio de estado con todas las validaciones
    """
    def post(self, request, pk, *args, **kwargs):
        """
        Procesa la solicitud de cambio de estado de búsqueda realizando:
        1. Verificación de permisos (solo el líder puede modificar)
        2. Validación de participación en torneos en curso
        3. Verificación de capacidad en torneos próximos
        4. Cambio de estado si se cumplen las condiciones
        5. Redirección con mensajes de retroalimentación

        Args:
            request: Objeto HttpRequest
            pk: ID del equipo a modificar
            *args: Argumentos variables
            **kwargs: Argumentos clave variables

        Returns:
            HttpResponseRedirect: Redirección a la vista de detalle del equipo
        """
        team = get_object_or_404(Team, pk=pk)
        player = Player.objects.get(user=request.user)

        if team.leader != player:
            messages.error(request, "No tienes permiso para modificar este equipo.")
            return redirect('web:playerTeamDetailView', pk=player.pk)

        if not team.searching_teammates:
            ongoing_tournaments = team.tournament_set.filter(status='Ongoing')
            if ongoing_tournaments.exists():
                messages.error(
                    request,
                    "No puedes activar la búsqueda de jugadores mientras el equipo esté participando en un torneo en curso."
                )
                return redirect('web:playerTeamDetailView', pk=player.pk)

            upcoming_tournaments = team.tournament_set.filter(status='Upcoming')
            for tournament in upcoming_tournaments:
                if team.player_set.count() >= tournament.max_players_per_team:
                    messages.error(
                        request,
                        f"No puedes activar la búsqueda de jugadores porque el equipo ya está completo en el torneo '{tournament.name}'."
                    )
                    return redirect('web:playerTeamDetailView', pk=player.pk)

        team.searching_teammates = not team.searching_teammates
        team.save()

        if team.searching_teammates:
            messages.success(request, "La búsqueda de jugadores ha sido activada.")
        else:
            messages.success(request, "La búsqueda de jugadores ha sido desactivada.")

        return redirect('web:playerTeamDetailView', pk=player.pk)

```
## 📝 Vista `MatchDetailView` – Detalles de un Partido

Muestra la información detallada de un partido específico ⚔️, incluyendo funcionalidades adaptadas a los jugadores que participan en él.

### 🔐 Requiere Autenticación

Solo usuarios autenticados pueden acceder a esta vista gracias al uso de `LoginRequiredMixin`.

### 🧠 ¿Qué ofrece esta vista?

1. 📋 Muestra los detalles completos del partido (equipos, fecha, etc.).
2. 🎮 Verifica si el usuario es jugador de alguno de los equipos participantes.
3. 📝 Si el usuario participa, se le muestra un **formulario para reportar el resultado del partido**.
4. ✅ Añade al contexto dos banderas clave:
   - `team_ready`: Indica si el equipo del jugador está marcado como "listo".
   - `team_confirmed`: Indica si el equipo ha confirmado el partido.
     
### 🧩 Contexto Personalizado

El contexto enviado al template incluye:

- `user_is_player`: `True` si el usuario pertenece a alguno de los equipos del partido.
- `form`: Formulario para enviar resultados (solo para jugadores involucrados).
- `team_ready`: Estado de preparación del equipo del jugador.
- `team_confirmed`: Estado de confirmación del equipo del jugador.

### 📎 Resultado Esperado

Los jugadores involucrados verán más opciones que un espectador regular, lo que permite una experiencia dinámica y enfocada en la interacción deportiva.
```python
class MatchDetailView(LoginRequiredMixin, DetailView):
    """
    Vista que muestra los detalles de un partido específico, incluyendo información
    relevante para los jugadores participantes.

    Requiere autenticación (LoginRequiredMixin) y muestra los datos de un partido
    individual, con funcionalidad especial para los jugadores de los equipos
    involucrados.

    Atributos:
        model (Model): Modelo Match que contiene los datos del partido
        template_name (str): Ruta al template que renderiza la vista (web/match_detail.html)
        context_object_name (str): Nombre de la variable que contendrá el objeto Match
                                en el contexto del template

    Métodos heredados de DetailView:
        get_object: Obtiene el objeto Match basado en los parámetros de la URL
        get_context_data: Proporciona el contexto para renderizar el template
    """
    model = Match
    template_name = 'web/match_detail.html'
    context_object_name = 'match'

    def get_context_data(self, **kwargs):
        """
        Extiende el contexto base con información adicional sobre la participación
        del usuario actual en el partido.

        Returns:
            dict: Contexto que incluye:
                - user_is_player: Booleano indicando si el usuario es jugador de alguno de los equipos
                - form: Formulario para reportar resultados (solo para jugadores participantes)
                - team_ready: Estado de preparación del equipo del usuario
                - team_confirmed: Estado de confirmación del equipo del usuario
        """
        context = super().get_context_data(**kwargs)
        match = self.get_object()

        is_team1_player = match.team1.player_set.filter(user=self.request.user).exists()
        is_team2_player = match.team2.player_set.filter(user=self.request.user).exists()

        context['user_is_player'] = is_team1_player or is_team2_player

        if is_team1_player or is_team2_player:
            form = MatchResultForm()
            form.fields['team1_score'].label = f"Puntaje de {match.team1.name}"
            form.fields['team2_score'].label = f"Puntaje de {match.team2.name}"
            context['form'] = form

        if is_team1_player:
            context['team_ready'] = match.team1_ready
            context['team_confirmed'] = match.team1_confirmed
        elif is_team2_player:
            context['team_ready'] = match.team2_ready
            context['team_confirmed'] = match.team2_confirmed
        else:
            context['team_ready'] = False
            context['team_confirmed'] = False

        return context
```
## ✅ Vista `MatchConfirmView` – Confirmación de Resultados

Permite a los jugadores confirmar oficialmente el resultado de un partido. Realiza validaciones de integridad ⚖️ para asegurar la coherencia entre los reportes de ambos equipos.

### 🔐 Requiere Autenticación

Usa `LoginRequiredMixin` para restringir el acceso solo a usuarios autenticados.

### 🧠 ¿Qué hace esta vista?

1. 📩 Muestra un formulario para ingresar los puntajes y seleccionar al ganador.
2. 🎮 Verifica que el usuario pertenezca a uno de los equipos del partido.
3. 🛡️ Asegura que ambos equipos estén de acuerdo con el resultado.
4. 🚨 En caso de inconsistencias, se notifica al administrador por correo.
5. 🏅 Registra el ganador, actualiza estadísticas y otorga renombre a los jugadores.

### 🔁 Métodos Soportados

- `GET`: Muestra el formulario de confirmación.
- `POST`: Procesa el formulario enviado, valida la información y registra el resultado.

### 📊 Validaciones Clave

- ✅ Ambos equipos deben confirmar al mismo ganador.
- ❌ El ganador no puede tener un puntaje menor o igual que el perdedor.
- 📬 Si hay discrepancias, se notifica al soporte vía email.

### 🧩 Contexto y Resultados

- El formulario se muestra sobre la misma vista de detalle (`match_detail.html`).
- Si todo es válido, se registra el resultado con `record_match_result` y se crea un log del partido.
- Se actualiza el renombre de todos los jugadores por participación exitosa.

### 📎 Resultado Esperado

Una experiencia segura y transparente para confirmar partidos, promoviendo el juego justo y la resolución automática de resultados consensuados.

```python
class MatchConfirmView(LoginRequiredMixin, View):
    """
    Vista para confirmar el resultado de un partido.

    Maneja tanto la visualización del formulario de confirmación (GET)
    como el procesamiento de los resultados confirmados (POST). Incluye
    validaciones para asegurar la integridad de los resultados reportados.

    Métodos:
        dispatch: Obtiene el partido antes de procesar cualquier solicitud
        get: Muestra el formulario de confirmación de resultados
        post: Procesa la confirmación del resultado con todas las validaciones
    """
    def dispatch(self, request, *args, **kwargs):
        """
        Prepara la vista obteniendo el partido asociado.

        Args:
            request: Objeto HttpRequest
            *args: Argumentos variables
            **kwargs: Argumentos clave variables

        Returns:
            HttpResponse: Respuesta del método dispatch de la superclase
        """
        self.match = get_object_or_404(Match, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Procesa la confirmación del resultado del partido realizando:
        1. Validación del formulario
        2. Verificación de pertenencia al equipo
        3. Registro de confirmación por equipo
        4. Validación de consistencia entre confirmaciones
        5. Actualización de estadísticas y registro final

        Args:
            request: Objeto HttpRequest con los datos del formulario
            *args: Argumentos variables
            **kwargs: Argumentos clave variables

        Returns:
            HttpResponseRedirect: Redirección a la vista de detalle del partido
        """
        match = self.match
        form = MatchResultForm(request.POST)

        if not form.is_valid():
            return render(request, 'web/match_detail.html', {
                'form': form,
                'match': match
            })

        # Verificar si el usuario pertenece a uno de los equipos
        user_team = request.user.player.team
        if user_team != match.team1 and user_team != match.team2:
            return HttpResponse('No estás en ninguno de los equipos de este partido', status=403)

        winner = form.cleaned_data['winner']
        team1_score = form.cleaned_data['team1_score']
        team2_score = form.cleaned_data['team2_score']

        # Marcar la confirmación del equipo
        if user_team == match.team1:
            match.team1_confirmed = True
            match.team1_winner = (winner == 'team1')
            create_match_log(match, f"Equipo 1 ({match.team1.name}) ha confirmado el resultado.", team=match.team1)

        elif user_team == match.team2:
            match.team2_confirmed = True
            match.team2_winner = (winner == 'team2')
            create_match_log(match, f"Equipo 2 ({match.team2.name}) ha confirmado el resultado.", team=match.team2)

        # Verificar si ambos equipos han confirmado el resultado
        if match.team1_confirmed and match.team2_confirmed:
            # Comparar si ambos equipos están de acuerdo con el ganador
            if match.team1_winner != match.team2_winner:
                # Enviar un correo de notificación al soporte si los equipos no están de acuerdo
                send_mail(
                    'Inconsistencia en el resultado del partido',
                    f'El partido {match.id} tiene un desacuerdo entre los equipos sobre el ganador.\n\n'
                    f'Equipo 1 seleccionado como ganador: {match.team1_winner}\n'
                    f'Equipo 2 seleccionado como ganador: {match.team2_winner}',
                    settings.DEFAULT_FROM_EMAIL,  # Remitente
                    [settings.SUPPORT_EMAIL],  # Correo de soporte
                    fail_silently=False
                )
                # Agregar el mensaje de error al formulario
                messages.error(request, 'Los dos equipos no están de acuerdo sobre el ganador. El administrador ha sido notificado.')
                return render(request, 'web/match_detail.html', {
                    'form': form,
                    'match': match
                })

            # Verificar que el puntaje sea coherente con el ganador
            if winner == 'team1' and team1_score <= team2_score:
                send_mail(
                    'Inconsistencia en el puntaje del partido',
                    f'El equipo 1 no puede ganar con un puntaje inferior o igual al del equipo 2. Partido ID: {match.id}\n\n'
                    f'Puntaje del equipo 1: {team1_score}, Puntaje del equipo 2: {team2_score}',
                    settings.DEFAULT_FROM_EMAIL,  # Remitente
                    [settings.SUPPORT_EMAIL],  # Correo de soporte
                    fail_silently=False
                )
                messages.error(request, 'El equipo 1 no puede ganar con un puntaje inferior o igual al del equipo 2. El administrador ha sido notificado.')
                return render(request, 'web/match_detail.html', {
                    'form': form,
                    'match': match
                })

            elif winner == 'team2' and team2_score <= team1_score:
                send_mail(
                    'Inconsistencia en el puntaje del partido',
                    f'El equipo 2 no puede ganar con un puntaje inferior o igual al del equipo 1. Partido ID: {match.id}\n\n'
                    f'Puntaje del equipo 1: {team1_score}, Puntaje del equipo 2: {team2_score}',
                    settings.DEFAULT_FROM_EMAIL,  # Remitente
                    [settings.SUPPORT_EMAIL],  # Correo de soporte
                    fail_silently=False
                )
                messages.error(request, 'El equipo 2 no puede ganar con un puntaje inferior o igual al del equipo 1. El administrador ha sido notificado.')
                return render(request, 'web/match_detail.html', {
                    'form': form,
                    'match': match
                })

            # Si ambos equipos han confirmado y los resultados son coherentes
            if match.team1_winner:
                match.winner = match.team1
                update_players_stats(match.team1, is_winner=True)
                update_players_stats(match.team2)  # Los jugadores del equipo perdedor también se actualizan

            elif match.team2_winner:
                match.winner = match.team2
                update_players_stats(match.team2, is_winner=True)
                update_players_stats(match.team1)  # Los jugadores del equipo perdedor también se actualizan

            # Aumentar el renombre a todos los jugadores del partido
            for player in match.team1.player_set.all():
                increase_player_renombre(player, amount=5, reason="Participación en partido completado con éxito")

            for player in match.team2.player_set.all():
                increase_player_renombre(player, amount=5, reason="Participación en partido completado con éxito")


            # Llamar a la función `record_match_result` para guardar el resultado
            record_match_result(match, match.winner, team1_score, team2_score)
            create_match_log(match, "El partido ha sido completado. Ganador: " + match.winner.name)

        match.save()

        # Redirigir a la vista de detalles del partido
        return redirect('web:matchDetailView', pk=match.id)

    def get(self, request, *args, **kwargs):
        """
        Muestra el formulario de confirmación de resultados.

        Args:
            request: Objeto HttpRequest
            *args: Argumentos variables
            **kwargs: Argumentos clave variables

        Returns:
            HttpResponse: Renderizado del template con el formulario
        """
        match = self.match
        form = MatchResultForm(initial={
            'team1_score': 1,  # Valor predeterminado para el puntaje de team1
            'team2_score': 1,  # Valor predeterminado para el puntaje de team2
        })

        return render(request, 'web/match_detail.html', {
            'form': form,
            'match': match
        })
```
---
## 🚪 Vista `LeaveTournamentView` – Abandonar Torneo

Permite que el **líder de un equipo** abandone un torneo en nombre de su equipo. Utiliza un formulario POST para confirmar la acción y está protegida por autenticación.

### 🔐 Requiere Autenticación

Gracias a `LoginRequiredMixin`, **solo los usuarios logueados** pueden intentar salir de un torneo. Si no has iniciado sesión, se te redirige al login.

### ✅ Requisitos para salir del torneo

Para que el usuario pueda abandonar el torneo, deben cumplirse todas estas condiciones:

1. El jugador **debe pertenecer a un equipo** 🧑‍🤝‍🧑
2. Su equipo **debe estar registrado en el torneo** 🏆
3. El jugador **debe ser el líder** del equipo 👑

Si alguna condición falla, se muestra un mensaje de advertencia y se redirige al detalle del torneo.

### 📤 ¿Qué hace?

- Elimina la instancia de `TournamentTeam`, desvinculando al equipo del torneo.
- Muestra un mensaje de éxito: _"Has abandonado el torneo"_
- Redirige a la vista de detalle del torneo.

### 🧾 Detalles Técnicos

- 🧱 Modelo afectado: `TournamentTeam`
- 🔄 Método usado: `POST`
- 📄 Template opcional para confirmación: `leave_tournament_confirm.html`
- 🔁 Redirección final: `web:tournamentDetailView` del torneo correspondiente

```python
class LeaveTournamentView(LoginRequiredMixin, TemplateView):
    """
    Vista para que un jugador abandone un torneo.

    Requiere autenticación y muestra una página de confirmación antes
    de procesar la solicitud de abandono del torneo.

    Atributos:
        template_name (str): Ruta al template de confirmación

    Métodos:
        post: Procesa la solicitud de abandono del torneo
    """
    template_name = 'web/leave_tournament_confirm.html'
    template_name = 'web/leave_tournament_confirm.html'  # si quieres una página de confirmación

    def post(self, request, *args, **kwargs):
        """
        Procesa la solicitud POST para abandonar un torneo:
        1. Verifica que el jugador pertenezca a un equipo
        2. Verifica que el equipo esté registrado en el torneo
        3. Verifica que el jugador sea el líder del equipo
        4. Elimina al equipo del torneo si se cumplen las condiciones

        Args:
            request: Objeto HttpRequest
            *args: Argumentos variables
            **kwargs: Argumentos clave variables (contiene 'pk' del torneo)

        Returns:
            HttpResponseRedirect: Redirección a la vista de detalle del torneo
        """
        tournament_id = self.kwargs['pk']
        tournament = get_object_or_404(Tournament, pk=tournament_id)
        player = get_object_or_404(Player, user=request.user)

        team = player.team
        if not team:
            messages.warning(request, "No estás en ningún equipo.")
            return redirect('web:tournamentDetailView', tournament.id)

        tt = TournamentTeam.objects.filter(tournament=tournament, team=team).first()
        if not tt:
            messages.warning(request, "Tu equipo no pertenece a este torneo.")
            return redirect('web:tournamentDetailView', tournament.id)

        if player != team.leader:
            messages.warning(request, "No eres el líder de tu equipo, no puedes realizar esta acción.")
            return redirect('web:tournamentDetailView', tournament.id)

        # Quitar al jugador del equipo
        tt.delete()
        messages.success(request, "Has abandonado el torneo.")

        return redirect('web:tournamentDetailView', tournament.id)
```
---

## 🔄 Navegación
[⬅️ Volver al README principal](../README.md)
