from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=10,
        choices=[('player', 'Player'), ('admin', 'Admin')],
        default='player'
    )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"

class Game(models.Model):
    name = models.CharField(max_length=100, unique=True)
    genre = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Tournament(models.Model):
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
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    games_played = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)
    winrate = models.FloatField(default=0.0)  # Nuevo campo de Winrate (%)

    def update_winrate(self):
        """Calcula y actualiza el winrate basado en las partidas jugadas."""
        if self.games_played > 0:
            self.winrate = (self.games_won / self.games_played) * 100
        else:
            self.winrate = 0.0
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.team.name} (Winrate: {self.winrate:.2f}%)"


class TournamentTeam(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    seed = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('tournament', 'team')

class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    round = models.IntegerField()
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2')
    scheduled_at = models.DateTimeField()
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('ongoing', 'Ongoing'), ('completed', 'Completed')],
        default='pending'
    )

class MatchResult(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE)
    winner = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    team1_score = models.IntegerField(default=0)
    team2_score = models.IntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)

class MatchLog(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    event = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
