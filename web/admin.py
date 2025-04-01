from django.contrib import admin
from .models import *
from django.utils.html import format_html

# Configuración del administrador para el modelo Game
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre', 'created_at', 'image_preview', 'image_url')
    search_fields = ('name', 'genre',)
    list_filter = ('genre',)

    def image_preview(self, obj):
        """Muestra una miniatura de la imagen en el panel de administración."""
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 5px;" />',
                               obj.image.url)
        return "No image"

    image_preview.short_description = "Imagen"

    def image_url(self, obj):
        """Muestra la URL de la imagen en el admin de Django."""
        if obj.image:
            return obj.image.url
        return "No image"

    image_url.short_description = "Imagen URL"

# Configuración del administrador para el modelo Tournament
@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'game', 'status', 'description', 'start_date', 'end_date', 'created_by')
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
    list_display = ('user', 'team', 'role', 'country', 'coins', 'renombre', 'mmr', 'games_played', 'games_won', 'winrate_preview', 'avatar_preview', 'avatar_url')
    list_filter = ('role', 'team', 'country')  # Permite filtrar por rol, comunidad y equipo
    search_fields = ('user__username', 'team__name')  # Permite buscar por nombre de usuario o nombre de equipo
    list_editable = ('role', 'country', 'coins', 'renombre')  # Permite editar el rol, comunidad, puntos y honor directamente desde la lista

    def winrate_preview(self, obj):
        return f"{obj.winrate:.0f}%"  # Redondea a 0 decimales

    winrate_preview.short_description = 'Winrate'  # Personaliza el título de la columna

    def avatar_preview(self, obj):
        """Muestra una miniatura de la imagen en el panel de administración."""
        if obj.avatar:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 5px;" />',
                               obj.avatar.url)
        return "No image"

    avatar_preview.short_description = "Avatar"

    def avatar_url(self, obj):
        """Muestra la URL de la imagen en el admin de Django."""
        if obj.avatar:
            return obj.avatar.url
        return "No image"

    avatar_url.short_description = "Avatar URL"

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


# Configuración del administrador para el modelo Reward
@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('name', 'coins_cost', 'stock', 'is_active', 'image_preview', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_active',)

    def image_preview(self, obj):
        """Muestra una miniatura de la imagen en el panel de administración."""
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 5px;" />', obj.image.url)
        return "No image"

    image_preview.short_description = "Image Preview"


# Configuración del administrador para el modelo Redemption
@admin.register(Redemption)
class RedemptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'reward', 'redeemed_at')
    search_fields = ('user__username', 'reward__name')
    list_filter = ('redeemed_at',)