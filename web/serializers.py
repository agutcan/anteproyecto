from rest_framework import serializers
from .models import Tournament

class TournamentSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='name')
    start = serializers.DateTimeField(source='start_date', format='%Y-%m-%dT%H:%M:%S')
    end = serializers.DateTimeField(source='end_date', format='%Y-%m-%dT%H:%M:%S')

    class Meta:
        model = Tournament
        fields = ["id", "title", "game", "start", "end", "description"]
