from django.contrib import admin
from .models import *

# Configuración del administrador para el modelo Game
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre', 'created_at')
    search_fields = ('name', 'genre')
    list_filter = ('genre',)

# Configuración del administrador para el modelo Tournament
@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'game', 'status', 'start_date', 'end_date', 'created_by')
    search_fields = ('name', 'game__name', 'created_by__username')
    list_filter = ('status', 'game')

# Configuración del administrador para el modelo Team
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)

# Configuración del administrador para el modelo Player
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    # Personalizamos el formulario para que se muestren ciertos campos
    list_display = ('user', 'team', 'role', 'games_played', 'games_won', 'winrate')
    list_filter = ('role', 'team')  # Permite filtrar por rol y equipo
    search_fields = ('user__username', 'team__name')  # Permite buscar por nombre de usuario o nombre de equipo
    list_editable = ('role',)  # Permite editar el rol directamente desde la lista

# Configuración del administrador para el modelo TournamentTeam
@admin.register(TournamentTeam)
class TournamentTeamAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'team', 'seed')
    search_fields = ('tournament__name', 'team__name')
    list_filter = ('tournament',)

# Configuración del administrador para el modelo Match
@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'round', 'team1', 'team2', 'scheduled_at', 'status')
    search_fields = ('tournament__name', 'team1__name', 'team2__name')
    list_filter = ('status', 'tournament')

# Configuración del administrador para el modelo MatchResult
@admin.register(MatchResult)
class MatchResultAdmin(admin.ModelAdmin):
    list_display = ('match', 'winner', 'team1_score', 'team2_score', 'completed_at')
    search_fields = ('match__team1__name', 'match__team2__name')
    list_filter = ('completed_at',)

# Configuración del administrador para el modelo MatchLog
@admin.register(MatchLog)
class MatchLogAdmin(admin.ModelAdmin):
    list_display = ('match', 'team', 'player', 'event', 'created_at')
    search_fields = ('match__team1__name', 'match__team2__name', 'player__user__username')
    list_filter = ('created_at',)

