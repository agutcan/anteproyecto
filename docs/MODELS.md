# 📄 Explicación de Modelos en Django (`models.py`)

Este archivo define los modelos utilizados en la aplicación web. Los modelos representan las tablas de la base de datos y sus relaciones. A continuación, se describen cada uno de los modelos:

---

## 🕹️ **Game**
Modelo que representa un videojuego dentro de la plataforma.

### 🧩 Campos:
- `name`: El nombre del juego (único).
- `genre`: Género del juego (opcional).
- `created_at`: Fecha de creación del juego (autogenerada).
- `image`: Imagen del juego (opcional).

```python
class Game(models.Model):
    """Modelo que representa un videojuego en el sistema.
    
    Atributos:
        name: Nombre único del juego (CharField)
        genre: Género del juego (opcional)
        created_at: Fecha de creación automática
        image: Imagen del juego con valor por defecto
    """
    
    name = models.CharField(max_length=100, unique=True)
    genre = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='games', blank=True, null=True, default='games/default_game.webp')

    def __str__(self):
        """Representación en cadena del juego (devuelve el nombre)"""
        return self.name
```

## 🏆 **Tournament**
Modelo que representa un torneo dentro de la plataforma.

### 🧩 Campos:
- `name`: Nombre del torneo.
- `game`: Relación con el modelo `Game` (juego que se juega en el torneo).
- `description`: Descripción del torneo.
- `status`: Estado del torneo, puede ser "upcoming", "ongoing", o "completed".
- `prize_pool`: Valor del premio en el torneo (opcional).
- `start_date`: Fecha y hora en que comienza el torneo.
- `created_by`: Usuario que creó el torneo (relación con el modelo `User`).
- `max_player_per_team`: Número máximo, tambien usado como mínimo, de jugadores permitidos por equipo.
- `max_teams`: Número máximo de equipos que pueden registrarse.
- `matches_generated`: Indica si los partidos han sido generados.
- `winner`: El equipo ganador del torneo (relación con el modelo `Team`).

### 🧠 Métodos importantes:
- `count_registered_players()`: Devuelve el número total de jugadores registrados en el torneo.
- `get_max_total_players()`: Devuelve el número máximo teórico de jugadores que pueden participar en el torneo.
- `get_available_slots()`: Calcula los espacios disponibles para la inscripción de jugadores en el torneo.
- `get_registered_teams()`: Devuelve los equipos registrados en el torneo.

### ✅ Validaciones:
- **Número de equipos**: El número máximo de equipos debe ser 2, 4 u 8.
- **Fecha de inicio**: La fecha de inicio no puede ser en el pasado.

```python
class Tournament(models.Model):
    """
    Modelo que representa un torneo de videojuegos en el sistema.
    
    Atributos:
        name: Nombre del torneo (requerido)
        game: Juego asociado (relación ForeignKey a Game)
        description: Descripción opcional del torneo
        status: Estado actual del torneo (upcoming/ongoing/completed)
        prize_pool: Premio total en dinero (opcional)
        start_date: Fecha y hora de inicio (requerido)
        created_by: Usuario que creó el torneo
        max_player_per_team: Jugadores por equipo
        max_teams: Número máximo de equipos permitidos
        matches_generated: Indica si los partidos están generados
        winner: Equipo ganador (se establece al finalizar)
    """
    
    name = models.CharField(max_length=100)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True, null=True, default='Torneo...')
    status = models.CharField(
        max_length=10,
        choices=[('upcoming', 'Upcoming'), ('ongoing', 'Ongoing'), ('completed', 'Completed')],
        default='upcoming'
    )
    prize_pool = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    start_date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    max_player_per_team = models.PositiveIntegerField(default=1)
    max_teams = models.PositiveIntegerField(default=2)
    matches_generated = models.BooleanField(default=False)
    winner = models.ForeignKey("Team", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        """Representación legible del torneo (nombre + estado)"""
        return f"{self.name} ({self.get_status_display()})"

    def count_registered_players(self):
        """
        Calcula el número total de jugadores registrados en el torneo.
        
        Returns:
            int: Cantidad de jugadores únicos registrados
        """
        from django.db.models import Count
        return self.tournamentteam_set.aggregate(
            total_players=Count('team__player', distinct=True)
        )['total_players'] or 0

    def get_max_total_players(self):
        """
        Calcula la capacidad máxima teórica de jugadores.
        
        Returns:
            int: max_teams * max_player_per_team
        """
        return self.max_teams * self.max_player_per_team

    def get_available_slots(self):
        """
        Calcula los espacios disponibles para nuevos jugadores.
        
        Returns:
            int: Diferencia entre capacidad máxima y jugadores registrados
        """
        return max(0, self.get_max_total_players() - self.count_registered_players())

    def get_registered_teams(self):
        """
        Obtiene la lista de equipos registrados en el torneo.
        
        Returns:
            list: Lista de objetos Team registrados
        """
        return [tt.team for tt in self.tournamentteam_set.all()]

    def clean(self):
        """
        Validaciones adicionales del modelo:
        - Verifica que max_teams sea 2, 4 u 8
        - Comprueba que start_date no sea en el pasado
        """
        super().clean()

        if self.max_teams not in {2, 4, 8}:
            raise ValidationError(
                {'max_teams': 'El número de equipos debe ser (2, 4 u 8) para el formato de eliminatorias.'}
            )

        if self.start_date and self.start_date < timezone.now():
            raise ValidationError("La fecha de inicio no puede ser en el pasado")
```

## 👥 **Team**
Modelo que representa un equipo dentro de la plataforma.

### 🧩 Campos:
- `name`: Nombre del equipo (único).
- `created_at`: Fecha de creación del equipo.

### 🧠 Métodos importantes:
- `get_avg_mmr()`: Calcula el promedio de MMR (Matchmaking Rating) de los jugadores que pertenecen a este equipo. Si el equipo no tiene jugadores, devuelve 0.

```python
class Team(models.Model):
    """Modelo que representa un equipo de jugadores.
    
    Atributos:
        name: Nombre único del equipo (CharField)
        created_at: Fecha de creación automática (DateTimeField)
        leader: Relación OneToOne con el jugador líder (Player)
        searching_teammates: Booleano que indica si buscan miembros
    """
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    leader = models.OneToOneField(
        "Player", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='led_team'
    )
    searching_teammates = models.BooleanField(default=False)

    def __str__(self):
        """Representación en string del equipo (devuelve el nombre)"""
        return self.name

    def get_avg_mmr(self):
        """Calcula el MMR promedio de los jugadores del equipo.
        
        Returns:
            float: Promedio de MMR o 0 si no tiene jugadores
        """
        players = self.player_set.all()
        if not players:
            return 0
        return sum(player.mmr for player in players) / players.count()
```

## 🎮 **Player**
Modelo que representa a un jugador en la plataforma.

### 🧩 Campos:
- `user`: Relación con el modelo `User`. Representa el usuario relacionado con el jugador.
- `team`: Relación con el modelo `Team`. Representa el equipo al que pertenece el jugador (puede ser `null` si no pertenece a un equipo).
- `role`: Define el rol del jugador. Puede ser "Premium" o "Normal".
- `first_name`: Nombre del jugador (opcional).
- `last_name`: Apellido del jugador (opcional).
- `birth_date`: Fecha de nacimiento del jugador (opcional).
- `country`: País del jugador, con opciones predefinidas como Argentina, Brasil, España, México, etc.
- `bio`: Biografía o descripción adicional del jugador (opcional).
- `avatar`: Imagen de perfil del jugador (opcional, con una imagen predeterminada por defecto).
- `coins`: Cantidad de monedas del jugador, que podría usarse en un sistema de recompensas.
- `renombre`: Un valor que representa el renombre del jugador, en un rango de 1 a 100.
- `mmr`: Rating de Matchmaking (MMR) del jugador. Se utiliza para medir el nivel de habilidad del jugador.
- `games_played`: Número de juegos jugados por el jugador.
- `games_won`: Número de juegos ganados por el jugador.
- `winrate`: Porcentaje de victorias del jugador calculado en base a los juegos jugados y ganados.

```python
class Player(models.Model):
    """Modelo que representa un jugador en el sistema.
    
    Atributos:
        user: Relación OneToOne con el modelo User de Django
        team: Equipo al que pertenece el jugador (opcional)
        role: Rol del jugador (Premium/Normal)
        first_name: Nombre del jugador (opcional)
        last_name: Apellido del jugador (opcional)
        birth_date: Fecha de nacimiento (opcional)
        country: País de origen (selección entre opciones)
        bio: Biografía/descripción del jugador (opcional)
        avatar: Imagen de perfil del jugador
        coins: Monedas virtuales del jugador
        renombre: Puntuación de reputación (1-100)
        mmr: Match Making Rating (valor mínimo 10)
        games_played: Total de partidas jugadas
        games_won: Total de partidas ganadas
        winrate: Porcentaje de victorias
    """
    
    # Relaciones con otros modelos
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)

    # Roles de los jugadores
    PREMIUM = 'Premium'
    DEFAULT = 'Normal'
    ROLE_CHOICES = [
        (PREMIUM, 'Premium'),
        (DEFAULT, 'Normal'),
    ]
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=DEFAULT,
    )

    # Información personal
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    # País de origen
    COUNTRY_CHOICES = [
        ('AR', 'Argentina'),
        ('BR', 'Brasil'),
        ('CL', 'Chile'),
        ('CO', 'Colombia'),
        ('ES', 'España'),
        ('MX', 'México'),
        ('US', 'Estados Unidos'),
    ]
    country = models.CharField(
        max_length=2,
        choices=COUNTRY_CHOICES,
        default='ES'
    )

    # Perfil y estadísticas
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='avatars/default_avatar.png')
    coins = models.IntegerField(default=0)
    renombre = models.IntegerField(default=50, validators=[MinValueValidator(1), MaxValueValidator(100)])
    mmr = models.IntegerField(default=50, validators=[MinValueValidator(10)])
    
    # Estadísticas de juego
    games_played = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)
    winrate = models.FloatField(default=0.0)

    def __str__(self):
        """Representación en string del jugador (username + equipo + winrate)."""
        return f"{self.user.username} - {self.team.name if self.team else 'Sin equipo'} (Winrate: {self.winrate:.2f}%)"

```

## 🏆 **TournamentTeam**
Este modelo representa la relación entre un torneo y un equipo que está inscrito en él.

### 🧩 Campos:
- `tournament`: Relación con el modelo `Tournament`, que representa el torneo en el que el equipo está participando.
- `team`: Relación con el modelo `Team`, que representa el equipo que se ha inscrito en el torneo.

### 🚫 Restricciones:
- **`unique_together`**: La combinación de `tournament` y `team` debe ser única. Esto significa que un equipo no puede inscribirse más de una vez en el mismo torneo.

### 📘 Descripción:
Este modelo se utiliza para asociar un equipo a un torneo específico. La relación es una asociación de muchos a muchos, ya que un equipo puede participar en varios torneos y un torneo puede tener múltiples equipos.

```python
class TournamentTeam(models.Model):
    """Modelo que relaciona equipos con torneos (tabla intermedia M2M).
    
    Atributos:
        tournament (ForeignKey): Torneo al que se inscribe el equipo
        team (ForeignKey): Equipo que participa en el torneo
    """
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        # Evita duplicados de equipo en el mismo torneo
        unique_together = ('tournament', 'team')

    def __str__(self):
        """Representación: '[Nombre equipo] en [Nombre torneo]'"""
        return f"{self.team.name} en {self.tournament.name}"
```

## ⚔️ **Match**
Este modelo representa una partida entre dos equipos dentro de un torneo. Cada partida se juega entre dos equipos y tiene un estado asociado (pendiente, en curso o completado).

### 🧩 Campos:
- `tournament`: Relación con el modelo `Tournament`, que representa el torneo al que pertenece la partida.
- `round`: Un número entero que indica la ronda de la partida dentro del torneo (por ejemplo, ronda 1, semifinal, final, etc.).
- `team1`: Relación con el modelo `Team`, que representa el primer equipo que juega en la partida.
- `team2`: Relación con el modelo `Team`, que representa el segundo equipo que juega en la partida.
- `winner`: Relación con el modelo `Team`, que almacena el equipo ganador de la partida. Este campo puede ser `null` si la partida aún no ha terminado.
- `scheduled_at`: Fecha y hora programada para la partida.
- `status`: Un campo de texto que indica el estado de la partida. Puede tomar los siguientes valores:
  - `'pending'`: La partida está pendiente de jugar.
  - `'ongoing'`: La partida está en curso.
  - `'completed'`: La partida ha sido completada.
- `team1_ready`: Un campo booleano que indica si el equipo 1 está listo para comenzar la partida.
- `team2_ready`: Un campo booleano que indica si el equipo 2 está listo para comenzar la partida.
- `team1_confirmed`: Un campo booleano que indica si el equipo 1 ha confirmado los resultados al finalizar la partida.
- `team2_confirmed`: Un campo booleano que indica si el equipo 2 ha confirmado los resultados al finalizar la partida.
- `team1_winner`: Un campo booleano que indica si el equipo 1 ha ganado la partida (se marca después de la finalización).
- `team2_winner`: Un campo booleano que indica si el equipo 2 ha ganado la partida (se marca después de la finalización).

### 📘 Descripción:
Este modelo se utiliza para representar una partida entre dos equipos dentro de un torneo. El campo `status` ayuda a seguir el progreso de la partida. Los campos `team1_ready` y `team2_ready` permiten saber si ambos equipos están listos para jugar. Además, el sistema permite a ambos equipos confirmar el resultado de la partida y marcar al ganador a través de los campos `team1_confirmed`, `team2_confirmed`, `team1_winner` y `team2_winner`.

```python
class Match(models.Model):
    """Modelo que representa un partido dentro de un torneo.
    
    Atributos:
        tournament (ForeignKey): Torneo al que pertenece el partido
        round (IntegerField): Número de ronda del torneo
        team1 (ForeignKey): Primer equipo participante
        team2 (ForeignKey): Segundo equipo participante
        winner (ForeignKey): Equipo ganador (opcional)
        scheduled_at (DateTimeField): Fecha y hora programada
        status (CharField): Estado actual del partido
        team1_ready (BooleanField): Confirmación de preparación equipo 1
        team2_ready (BooleanField): Confirmación de preparación equipo 2
        team1_confirmed (BooleanField): Confirmación final equipo 1
        team2_confirmed (BooleanField): Confirmación final equipo 2
        team1_winner (BooleanField): Autodeclaración ganador equipo 1
        team2_winner (BooleanField): Autodeclaración ganador equipo 2
    """
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    round = models.IntegerField()
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_as_team1')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_as_team2')
    winner = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='matches_won')
    scheduled_at = models.DateTimeField()
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('ongoing', 'Ongoing'), ('completed', 'Completed')],
        default='pending'
    )
    team1_ready = models.BooleanField(default=False)
    team2_ready = models.BooleanField(default=False)
    team1_confirmed = models.BooleanField(default=False)
    team2_confirmed = models.BooleanField(default=False)
    team1_winner = models.BooleanField(default=False)
    team2_winner = models.BooleanField(default=False)

    def __str__(self):
        """Representación: 'Partido [ronda]: [equipo1] vs [equipo2] - [estado]'"""
        return f"Partido {self.round}: {self.team1.name} vs {self.team2.name} - {self.get_status_display()}"

```

## 📜 **MatchLog**
El modelo `MatchLog` se utiliza para registrar eventos o acciones que ocurren durante una partida, como los movimientos de jugadores, goles, cambios de estado, etc. Cada entrada en el `MatchLog` se asocia con una partida específica, y puede registrar eventos tanto a nivel de equipo como de jugador.

### 🧩 Campos:
- `match`: Relación con el modelo `Match`, que representa la partida en la que ocurrió el evento.
- `team`: Relación con el modelo `Team`, que indica el equipo involucrado en el evento. Este campo puede ser `null` si el evento no está asociado a un equipo específico.
- `player`: Relación con el modelo `Player`, que indica el jugador involucrado en el evento. Este campo puede ser `null` si el evento no está asociado a un jugador específico.
- `event`: Un campo de texto que describe el evento que ocurrió durante la partida (por ejemplo, "Jugador X marcó un gol", "Cambio de equipo").
- `created_at`: Fecha y hora en que el evento fue registrado en el sistema.

### 📘 Descripción:
El modelo `MatchLog` sirve para crear un registro detallado de todo lo que sucede durante una partida. Los eventos pueden ser variados, como la anotación de un gol, la expulsión de un jugador o incluso el comienzo o final de una partida. Este modelo ayuda a tener un seguimiento detallado de la dinámica del partido y también puede ser útil para generar informes o estadísticas.

Los campos `team` y `player` son opcionales, ya que algunos eventos pueden no estar directamente relacionados con un equipo o jugador (por ejemplo, un evento que simplemente indica que el partido ha comenzado). Sin embargo, cuando hay una acción específica de un equipo o jugador, se almacena esa relación para mayor claridad.

```python
class MatchLog(models.Model):
    """Modelo que registra eventos ocurridos durante una partida.
    
    Atributos:
        match (ForeignKey): Partida asociada al evento
        team (ForeignKey): Equipo relacionado (opcional)
        player (ForeignKey): Jugador relacionado (opcional)
        event (TextField): Descripción del evento registrado
        created_at (DateTimeField): Fecha de creación del registro
    """
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    event = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Representación: 'Log [partida]: - [evento]'"""
        return f"Log {self.match}: - {self.event}"
```

## 🏆 **MatchResult**
El modelo `MatchResult` representa los resultados de una partida dentro de un torneo. Este modelo se asocia de manera directa con el modelo `Match`, lo que significa que cada resultado está vinculado a una partida específica. Registra el puntaje de los dos equipos participantes, el ganador de la partida y la fecha en la que se completó el partido.

### 🧩 Campos:
- `match`: Relación de tipo `OneToOneField` con el modelo `Match`. Cada entrada en `MatchResult` corresponde a una única partida.
- `winner`: Relación con el modelo `Team`, que representa al equipo ganador de la partida. Este campo puede ser `null` si no se ha determinado el ganador.
- `team1_score`: Puntaje del equipo 1 en la partida.
- `team2_score`: Puntaje del equipo 2 en la partida.
- `completed_at`: Fecha y hora en la que el partido fue completado. Se establece automáticamente con la fecha y hora actuales cuando el resultado se guarda.

### 📘 Descripción:
El modelo `MatchResult` es utilizado para almacenar los resultados finales de las partidas en los torneos. Cada vez que una partida se termina, se crea un objeto `MatchResult` que almacena los puntajes de los equipos y el equipo ganador.

- El campo `winner` es opcional, ya que puede ser `null` en caso de que no se haya determinado un ganador aún (por ejemplo, en caso de empate o si el resultado no se ha registrado).
- Los campos `team1_score` y `team2_score` permiten almacenar los puntajes de los dos equipos.
- La fecha `completed_at` se llena automáticamente con la fecha en la que se crea el resultado.

```python
class MatchResult(models.Model):
    """Modelo que almacena los resultados de un partido.
    
    Atributos:
        match (OneToOneField): Partido asociado al resultado
        winner (ForeignKey): Equipo ganador (puede ser nulo)
        team1_score (IntegerField): Puntuación del equipo 1
        team2_score (IntegerField): Puntuación del equipo 2
        completed_at (DateTimeField): Fecha de finalización
    """
    match = models.OneToOneField(Match, on_delete=models.CASCADE)
    winner = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    team1_score = models.IntegerField(default=0)
    team2_score = models.IntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Representación: 'Resultado: [equipo1] [score1] - [score2] [equipo2]'"""
        return f"Resultado: {self.match.team1.name} {self.team1_score} - {self.team2_score} {self.match.team2.name}"

```

## 🎁 **Reward**
El modelo `Reward` representa recompensas que los usuarios pueden canjear utilizando monedas virtuales (`coins`). Este sistema está pensado para incentivar la participación, el rendimiento o la interacción dentro de la plataforma (por ejemplo, al ganar partidas o torneos).

### 🧩 Campos:
- `name`: Nombre de la recompensa. Campo obligatorio y de hasta 255 caracteres.
- `description`: Descripción detallada u opcional de la recompensa. Es un campo de texto libre y puede estar vacío.
- `coins_cost`: Cantidad de monedas necesarias para canjear esta recompensa. Por defecto es 100.
- `stock`: Cantidad disponible de esta recompensa. Cuando el stock llega a 0, no puede ser canjeada.
- `is_active`: Booleano que indica si la recompensa está activa o disponible para ser redimida.
- `created_at`: Fecha en la que se creó la recompensa. Se establece automáticamente al crearla.
- `updated_at`: Fecha en la que fue actualizada por última vez. Se actualiza automáticamente en cada cambio.
- `image`: Imagen representativa de la recompensa. Por defecto se asigna una imagen predeterminada (`default_reward.webp`).

### 📘 Descripción:
Este modelo permite definir recompensas intercambiables dentro de la plataforma. Los usuarios que hayan acumulado suficientes monedas (`coins`) pueden "comprarlas" mediante el modelo `Redemption`.

El campo `stock` permite gestionar la disponibilidad, asegurando que una recompensa no se canjee si no hay unidades restantes. Además, el campo `is_active` puede usarse para desactivar temporalmente una recompensa sin eliminarla.

```python
class Reward(models.Model):
    """Modelo que representa una recompensa/premio canjeable.
    
    Atributos:
        name (CharField): Nombre de la recompensa
        description (TextField): Descripción detallada (opcional)
        coins_cost (PositiveIntegerField): Costo en monedas virtuales
        stock (PositiveIntegerField): Cantidad disponible
        is_active (BooleanField): Indica si está disponible
        created_at (DateTimeField): Fecha de creación
        updated_at (DateTimeField): Fecha de última actualización
        image (ImageField): Imagen representativa
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    coins_cost = models.PositiveIntegerField(default=100)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to='rewards/', 
        blank=True, 
        null=True, 
        default='rewards/default_reward.webp'
    )

    def __str__(self):
        """Representación: '[nombre] ([costo] coins)'"""
        return f"{self.name} ({self.coins_cost} coins)"
```

## 🎟️ **Redemption**
El modelo `Redemption` representa el canje de una recompensa (`Reward`) por parte de un usuario (`User`). Este registro permite llevar un historial de transacciones en las que los usuarios gastan monedas virtuales para obtener recompensas.

### 🧩 Campos:
- `user`: Referencia al usuario que ha canjeado una recompensa. Relación many-to-one con `User`.
- `reward`: Referencia a la recompensa que fue canjeada. Relación many-to-one con `Reward`.
- `redeemed_at`: Fecha y hora en la que se realizó el canje. Se establece automáticamente al crear la redención.

### 📘 Descripción:
Cada vez que un usuario realiza un canje, se crea una instancia de `Redemption`. Esto permite:
- Llevar control del historial de canjes.
- Evitar duplicidad si se desea restringir canjes múltiples por usuario.
- Mostrar a los usuarios sus recompensas obtenidas.

El campo `related_name="redemptions"` en ambos `ForeignKey` permite acceder fácilmente a las redenciones desde el usuario o desde la recompensa:

```python
class Redemption(models.Model):
    """Modelo que registra el canje de recompensas por usuarios.
    
    Atributos:
        user (ForeignKey): Usuario que realiza el canje
        reward (ForeignKey): Recompensa canjeada
        redeemed_at (DateTimeField): Fecha de canje automática
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="redemptions"
    )
    reward = models.ForeignKey(
        Reward, 
        on_delete=models.CASCADE, 
        related_name="redemptions"
    )
    redeemed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Representación: '[usuario] redeemed [recompensa] on [fecha]'"""
        return f"{self.user.username} redeemed {self.reward.name} on {self.redeemed_at}"
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
- 🎯 [Workflows](WORKFLOWS.md)
- 🚀 [Compose](DOCKER-COMPOSE.md)
- ⬅️ [Volver al README principal](../README.md)

---

## 🔔 Nota sobre `Notification`

Se añadió el modelo `Notification` como eje del sistema de avisos.

### Qué guarda
- Usuario principal y destinatarios
- Título, mensaje y urgencia
- Estado de la cola de envío
- Fecha de lectura y de envío
- Relación opcional con torneo o partido

### Para qué se usa
- Avisos de soporte
- Torneos y partidos
- Gestión administrativa
- Cola de correo con Celery