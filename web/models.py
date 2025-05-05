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
    """Modelo para representar los juegos."""
    name = models.CharField(max_length=100, unique=True)
    genre = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='games', blank=True, null=True, default='games/default_game.webp')

    def __str__(self):
        return self.name


class Tournament(models.Model):
    """Modelo de torneo."""
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
        return f"{self.name} ({self.get_status_display()})"

    def count_registered_players(self):
        """Cuenta jugadores inscritos (optimizado para BD)"""
        from django.db.models import Count
        return self.tournamentteam_set.aggregate(
            total_players=Count('team__player', distinct=True)
        )['total_players'] or 0

    def get_max_total_players(self):
        """Máximo teórico de jugadores"""
        return self.max_teams * self.max_player_per_team

    def get_available_slots(self):
        """Slots disponibles para inscripción"""
        return max(0, self.get_max_total_players() - self.count_registered_players())

    def get_registered_teams(self):
        return [tt.team for tt in self.tournamentteam_set.all()]

    def clean(self):
        super().clean()

        # Validación de número par
        if self.max_teams != 2 and self.max_teams != 4 and self.max_teams != 8:
            raise ValidationError(
                {'max_teams': 'El número de equipos debe ser (2, 4 o 8) para el formato de eliminatorias.'}
            )

        # Otras validaciones del modelo
        if self.start_date:
            if self.start_date < timezone.now():
                raise ValidationError("La fecha de inicio no puede ser en el pasado")

class Team(models.Model):
    """Modelo de equipo."""
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    leader = models.OneToOneField("Player", on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='led_team')
    searching_teammates = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_avg_mmr(self):
        players = self.player_set.all()
        if not players:
            return 0
        return sum(player.mmr for player in players) / players.count()

class Player(models.Model):
    """Modelo para representar jugadores."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)

    # Roles de los jugadores (Premium o Normal)
    PREMIUM = 'Premium'
    DEFAULT = 'Normal'
    ROLE_CHOICES = [
        (PREMIUM, 'Premium'),
        (DEFAULT, 'Normal'),
    ]
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=DEFAULT,  # Por defecto, el rol es Normal
    )

    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

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
        default='ES'  # Puedes cambiar el país por defecto
    )
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='avatars/default_avatar.png')
    coins = models.IntegerField(default=0)
    renombre = models.IntegerField(default=50, validators=[MinValueValidator(1), MaxValueValidator(100)])
    mmr = models.IntegerField(default=50, validators=[MinValueValidator(10)])

    # Estadísticas
    games_played = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)
    winrate = models.FloatField(default=0.0)  # Winrate en porcentaje

    def update_winrate(self):
        """Calcula y actualiza el winrate."""
        if self.games_played > 0:
            self.winrate = (self.games_won / self.games_played) * 100
        else:
            self.winrate = 0.0
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.team.name if self.team else 'Sin equipo'} (Winrate: {self.winrate:.2f}%)"


class TournamentTeam(models.Model):
    """Equipos inscritos en un torneo."""
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('tournament', 'team')

    def __str__(self):
        return f"{self.team.name} en {self.tournament.name}"


class Match(models.Model):
    """Modelo de partidas dentro de un torneo."""
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
    team1_ready = models.BooleanField(default=False)  # Confirmación del equipo 1 (Para comenzar)
    team2_ready = models.BooleanField(default=False)  # Confirmación del equipo 2 (Para comenzar)
    team1_confirmed = models.BooleanField(default=False)  # Confirmación del equipo 1 (Para finalizar)
    team2_confirmed = models.BooleanField(default=False)  # Confirmación del equipo 2 (Para finalizar)
    team1_winner = models.BooleanField(default=False)  # Equipo 1 marca si es ganador
    team2_winner = models.BooleanField(default=False)  # Equipo 2 marca si es ganador

    def __str__(self):
        return f"Partido {self.round}: {self.team1.name} vs {self.team2.name} - {self.get_status_display()}"


class MatchResult(models.Model):
    """Resultados de un partido."""
    match = models.OneToOneField(Match, on_delete=models.CASCADE)
    winner = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    team1_score = models.IntegerField(default=0)
    team2_score = models.IntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resultado: {self.match.team1.name} {self.team1_score} - {self.team2_score} {self.match.team2.name}"


class MatchLog(models.Model):
    """Registro de eventos en una partida."""
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    event = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log {self.match}: - {self.event}"


class Reward(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    coins_cost = models.PositiveIntegerField(default=100)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='rewards/', blank=True, null=True, default='rewards/default_reward.webp')

    def __str__(self):
        return f"{self.name} ({self.coins_cost} coins)"

class Redemption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="redemptions")
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE, related_name="redemptions")
    redeemed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} redeemed {self.reward.name} on {self.redeemed_at}"
