from django.contrib import admin
from .models import *
from django.utils.html import format_html

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
        'truncated_description',  # Descripción abreviada
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
