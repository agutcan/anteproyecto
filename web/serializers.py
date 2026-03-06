from rest_framework import serializers
from .models import *

# class TournamentSerializer(serializers.ModelSerializer):
#     """
#     Serializador para el modelo Tournament que adapta los nombres de campos
#     para su uso en interfaces frontend.
#
#     Transformaciones:
#     - Campo 'name' del modelo → se expone como 'title'
#     - Campo 'start_date' del modelo → se expone como 'start' en formato ISO 8601
#
#     Campos incluidos:
#     - id: Identificador único del torneo
#     - title: Nombre del torneo (mapeado desde 'name')
#     - game: Juego asociado al torneo
#     - start: Fecha de inicio en formato YYYY-MM-DDTHH:MM:SS
#     """
#
#     title = serializers.CharField(
#         source='name',
#     )
#
#     start = serializers.DateTimeField(
#         source='start_date',
#         format='%Y-%m-%dT%H:%M:%S',
#     )
#
#     class Meta:
#         model = Tournament
#         fields = ["id", "title", "game", "start"]

class PlayerStatsSerializer(serializers.ModelSerializer):
    """Serializador para estadísticas públicas de jugadores
    
    Atributos expuestos:
        username (str): Nombre de usuario obtenido del modelo User relacionado
        games_won (int): Número total de partidas ganadas
        winrate (float): Porcentaje de victorias (0-100)
    
    Uso típico:
        - Tablas de clasificación
        - Perfiles públicos de jugadores
        - Componentes de estadísticas
    """
    username = serializers.CharField(
        source='user.username',
    )

    class Meta:
        model = Player
        fields = ['username', 'games_won', 'winrate']


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'name', 'genre', 'image', 'created_at']


class TeamSerializer(serializers.ModelSerializer):
    avg_mmr = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'leader', 'searching_teammates', 'created_at', 'avg_mmr']

    def get_avg_mmr(self, obj):
        return obj.get_avg_mmr()


class PlayerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    avatar = serializers.ImageField(allow_null=True, required=False)
    team = TeamSerializer(read_only=True)

    class Meta:
        model = Player
        fields = [
            'id', 'username', 'user', 'team', 'role', 'first_name', 'last_name',
            'birth_date', 'country', 'bio', 'avatar', 'coins', 'renombre', 'mmr',
            'games_played', 'games_won', 'winrate'
        ]
        read_only_fields = ['user']


class TournamentSerializer(serializers.ModelSerializer):
    game = GameSerializer(read_only=True)
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    winner = TeamSerializer(read_only=True)

    class Meta:
        model = Tournament
        fields = [
            'id', 'name', 'game', 'description', 'status', 'prize_pool',
            'start_date', 'created_by', 'max_player_per_team', 'max_teams',
            'matches_generated', 'winner'
        ]


class TournamentTeamSerializer(serializers.ModelSerializer):
    tournament = serializers.PrimaryKeyRelatedField(read_only=True)
    team = TeamSerializer(read_only=True)

    class Meta:
        model = TournamentTeam
        fields = ['id', 'tournament', 'team']


class MatchSerializer(serializers.ModelSerializer):
    tournament = serializers.PrimaryKeyRelatedField(read_only=True)
    team1 = TeamSerializer(read_only=True)
    team2 = TeamSerializer(read_only=True)
    winner = TeamSerializer(read_only=True)

    class Meta:
        model = Match
        fields = [
            'id', 'tournament', 'round', 'team1', 'team2', 'winner', 'scheduled_at',
            'status', 'team1_ready', 'team2_ready', 'team1_confirmed', 'team2_confirmed',
            'team1_winner', 'team2_winner'
        ]


class MatchResultSerializer(serializers.ModelSerializer):
    match = MatchSerializer(read_only=True)
    winner = TeamSerializer(read_only=True)

    class Meta:
        model = MatchResult
        fields = ['id', 'match', 'winner', 'team1_score', 'team2_score', 'completed_at']


class MatchLogSerializer(serializers.ModelSerializer):
    match = serializers.PrimaryKeyRelatedField(read_only=True)
    team = TeamSerializer(read_only=True)
    player = PlayerSerializer(read_only=True)

    class Meta:
        model = MatchLog
        fields = ['id', 'match', 'team', 'player', 'event', 'created_at']


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = ['id', 'name', 'description', 'coins_cost', 'stock', 'is_active', 'created_at', 'updated_at', 'image']


class RedemptionSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    reward = RewardSerializer(read_only=True)

    class Meta:
        model = Redemption
        fields = ['id', 'user', 'reward', 'redeemed_at']
