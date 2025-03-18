from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    """Modelo para representar los juegos."""
    name = models.CharField(max_length=100, unique=True)
    genre = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tournament(models.Model):
    """Modelo de torneo."""
    name = models.CharField(max_length=100)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=[('upcoming', 'Upcoming'), ('ongoing', 'Ongoing'), ('completed', 'Completed')],
        default='upcoming'
    )
    prize_pool = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"


class Team(models.Model):
    """Modelo de equipo."""
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    """Modelo para representar jugadores."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)

    # Roles de los jugadores (Capitán o Miembro)
    CAPTAIN = 'Capitán'
    MEMBER = 'Miembro'
    ROLE_CHOICES = [
        (CAPTAIN, 'Capitán'),
        (MEMBER, 'Miembro'),
    ]
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=MEMBER,  # Por defecto, el rol es Miembro
    )

    # Datos del perfil (Antes en Profile)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)

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
    seed = models.IntegerField(blank=True, null=True)

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
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    event = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log {self.match}: {self.player.user.username} - {self.event}"
