from sys import maxsize
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.


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

    def update_winrate(self):
        """Actualiza el porcentaje de victorias basado en games_played y games_won."""
        if self.games_played > 0:
            self.winrate = (self.games_won / self.games_played) * 100
        else:
            self.winrate = 0.0
        self.save()

    def __str__(self):
        """Representación en string del jugador (username + equipo + winrate)."""
        return f"{self.user.username} - {self.team.name if self.team else 'Sin equipo'} (Winrate: {self.winrate:.2f}%)"

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
