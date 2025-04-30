from rest_framework import serializers
from .models import *

class TournamentSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='name')
    start = serializers.DateTimeField(source='start_date', format='%Y-%m-%dT%H:%M:%S')

    class Meta:
        model = Tournament
        fields = ["id", "title", "game", "start"]

class PlayerStatsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Player
        fields = ['username', 'games_won', 'winrate']