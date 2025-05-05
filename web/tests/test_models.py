from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from tournament.models import *


class ModelTests(TestCase):

    def setUp(self):
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
        self.assertEqual(str(self.game), 'Test Game')

    def test_team_creation(self):
        self.assertEqual(str(self.team1), 'Team One')

    def test_player_creation(self):
        player = Player.objects.create(user=self.user, team=self.team1, mmr=100)
        self.assertEqual(player.team.name, 'Team One')
        self.assertIn('testuser', str(player))

    def test_tournament_creation(self):
        self.assertEqual(self.tournament.name, 'Test Tournament')
        self.assertEqual(str(self.tournament), 'Test Tournament (Upcoming)')

    def test_tournament_team_unique(self):
        TournamentTeam.objects.create(tournament=self.tournament, team=self.team1)
        with self.assertRaises(Exception):
            TournamentTeam.objects.create(tournament=self.tournament, team=self.team1)

    def test_match_creation(self):
        match = Match.objects.create(
            tournament=self.tournament,
            round=1,
            team1=self.team1,
            team2=self.team2,
            scheduled_at=timezone.now() + timedelta(days=2)
        )
        self.assertIn("Partido", str(match))

    def test_match_result_creation(self):
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
        reward = Reward.objects.create(name="Camisa", coins_cost=300, stock=10)
        self.assertEqual(str(reward), "Camisa (300 coins)")

    def test_redemption_creation(self):
        reward = Reward.objects.create(name="Gorra", coins_cost=100, stock=5)
        redemption = Redemption.objects.create(user=self.user, reward=reward)
        self.assertIn("testuser redeemed Gorra", str(redemption))

    def tearDown(self):
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
