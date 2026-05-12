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
        source="user.username",
    )

    class Meta:
        model = Player
        fields = ["username", "games_won", "winrate"]


class SupportChatMessageSerializer(serializers.Serializer):
    """Entrada para el chat de soporte."""

    message = serializers.CharField(max_length=1000)

    def validate_message(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El mensaje no puede estar vacío.")
        return value.strip()


class SupportChatResponseSerializer(serializers.Serializer):
    """Salida normalizada para el chat de soporte."""

    response = serializers.CharField()
    confidence = serializers.FloatField()
    should_escalate = serializers.BooleanField()
    sources = serializers.ListField(child=serializers.CharField(), required=False)


class NotificationSerializer(serializers.ModelSerializer):
    """Serializador para notificaciones."""

    sender_email = serializers.CharField(allow_null=True)
    recipients = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ["id", "title", "message", "urgency", "status", "created_at", "read_at", "sender_email", "recipients"]

    def get_recipients(self, obj):
        return [u.username for u in obj.recipient_users.all()]
