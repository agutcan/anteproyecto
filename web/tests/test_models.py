from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from tournament.models import *


from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from .models import (
    Game, Team, Player, Tournament, TournamentTeam,
    Match, MatchResult, MatchLog, Reward, Redemption
)

class ModelTests(TestCase):
    """
    Conjunto de pruebas unitarias para los modelos del sistema.
    Verifica la creación y funcionamiento básico de las entidades:
    juegos, equipos, jugadores, torneos, partidos, resultados, logs,
    recompensas y redenciones.
    """

    def setUp(self):
        """
        Configura los datos comunes para todas las pruebas.
        Se ejecuta antes de cada método de test.
        """
        self.user = User.objects.create_user(username='testuser')
        self.team1 = Team.objects.create(name='Team One')
        self.team2 = Team.objects.create(name='Team Two')
        self.game = Game.objects.create(name='Test Game')
        self.tournament = Tournament.objects.create(
            name='Test Tournament',
            game=self.game,
            start_date=timezone.now() + timedelta(days=1),
            created_by=self.user,
            max_teams=2
        )

    def test_game_creation(self):
        """Verifica que el juego se crea correctamente y su representación como string es válida."""
        self.assertEqual(str(self.game), 'Test Game')

    def test_team_creation(self):
        """Verifica que el equipo se crea correctamente y su representación como string es válida."""
        self.assertEqual(str(self.team1), 'Team One')

    def test_player_creation(self):
        """Crea un jugador y valida su asociación al equipo y su representación textual."""
        player = Player.objects.create(user=self.user, team=self.team1, mmr=100)
        self.assertEqual(player.team.name, 'Team One')
        self.assertIn('testuser', str(player))

    def test_tournament_creation(self):
        """Verifica que el torneo se crea correctamente y su estado inicial es 'Upcoming'."""
        self.assertEqual(self.tournament.name, 'Test Tournament')
        self.assertEqual(str(self.tournament), 'Test Tournament (Upcoming)')

    def test_tournament_team_unique(self):
        """
        Verifica que un equipo no puede inscribirse dos veces en el mismo torneo.
        Espera una excepción por la restricción de unicidad.
        """
        TournamentTeam.objects.create(tournament=self.tournament, team=self.team1)
        with self.assertRaises(Exception):
            TournamentTeam.objects.create(tournament=self.tournament, team=self.team1)

    def test_match_creation(self):
        """Crea un partido y verifica que su representación textual contiene la palabra 'Partido'."""
        match = Match.objects.create(
            tournament=self.tournament,
            round=1,
            team1=self.team1,
            team2=self.team2,
            scheduled_at=timezone.now() + timedelta(days=2)
        )
        self.assertIn("Partido", str(match))

    def test_match_result_creation(self):
        """Crea un resultado para un partido y verifica la asociación con el equipo ganador."""
        match = Match.objects.create(
            tournament=self.tournament,
            round=1,
            team1=self.team1,
            team2=self.team2,
            scheduled_at=timezone.now() + timedelta(days=2)
        )
        result = MatchResult.objects.create(
            match=match,
            winner=self.team1,
            team1_score=3,
            team2_score=1
        )
        self.assertEqual(result.winner, self.team1)
        self.assertIn("Resultado:", str(result))

    def test_match_log_creation(self):
        """Crea un log de evento en un partido y verifica que el texto del evento sea representado correctamente."""
        player = Player.objects.create(user=self.user, team=self.team1, mmr=100)
        match = Match.objects.create(
            tournament=self.tournament,
            round=1,
            team1=self.team1,
            team2=self.team2,
            scheduled_at=timezone.now() + timedelta(days=2)
        )
        log = MatchLog.objects.create(
            match=match,
            player=player,
            team=self.team1,
            event="Kill event"
        )
        self.assertIn("Kill event", str(log))

    def test_reward_creation(self):
        """Crea una recompensa y verifica su representación textual con nombre y coste en monedas."""
        reward = Reward.objects.create(name="Camisa", coins_cost=300, stock=10)
        self.assertEqual(str(reward), "Camisa (300 coins)")

    def test_redemption_creation(self):
        """Verifica que una redención de recompensa por un usuario se representa correctamente."""
        reward = Reward.objects.create(name="Gorra", coins_cost=100, stock=5)
        redemption = Redemption.objects.create(user=self.user, reward=reward)
        self.assertIn("testuser redeemed Gorra", str(redemption))

    def tearDown(self):
        """
        Limpia la base de datos eliminando todos los objetos creados.
        Se ejecuta después de cada test.
        """
        Redemption.objects.all().delete()
        Reward.objects.all().delete()
        MatchLog.objects.all().delete()
        MatchResult.objects.all().delete()
        Match.objects.all().delete()
        TournamentTeam.objects.all().delete()
        Player.objects.all().delete()
        Team.objects.all().delete()
        Tournament.objects.all().delete()
        Game.objects.all().delete()
        User.objects.all().delete()
