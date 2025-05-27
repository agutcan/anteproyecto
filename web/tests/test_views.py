from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.test import TestCase, Client
from rest_framework import status
from django.urls import reverse
from ..models import *
from ..serializers import PlayerStatsSerializer
from unittest.mock import patch
from ..forms import *
from django.utils import timezone
from datetime import timedelta

class PlayerStatsListAPITest(APITestCase):
    """
    Pruebas para la API que lista las estadísticas de los jugadores.

    Verifica que la respuesta de la API incluya correctamente los datos de los jugadores,
    que la estructura del JSON sea la esperada, y que el número de jugadores devueltos
    coincida con los creados.
    """

    def setUp(self):
        """
        Configura los datos de prueba antes de cada test:
        - Crea un equipo de prueba.
        - Crea dos usuarios y jugadores asociados con estadísticas distintas.
        - Define la URL de la vista que se probará.
        """
        Player.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()

        self.team = Team.objects.create(name="Test Team")

        self.user1 = User.objects.create_user(username='user1', password='testpass')
        self.user2 = User.objects.create_user(username='user2', password='testpass')

        self.player1 = Player.objects.create(
            user=self.user1,
            team=self.team,
            mmr=60,
            games_played=10,
            games_won=7,
            winrate=70.0
        )
        self.player2 = Player.objects.create(
            user=self.user2,
            team=self.team,
            mmr=50,
            games_played=12,
            games_won=5,
            winrate=41.7
        )

        self.url = reverse('web:playerStatsListApi')

    def test_get_all_player_stats(self):
        """
        Verifica que la API devuelve correctamente todas las estadísticas
        de los jugadores con un status HTTP 200 y datos equivalentes al serializer.
        """
        response = self.client.get(self.url)
        players = Player.objects.select_related('team', 'user').all()
        serializer = PlayerStatsSerializer(players, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)

    def test_player_count(self):
        """
        Verifica que la cantidad de jugadores devueltos por la API
        coincide con el número de jugadores creados (2).
        """
        response = self.client.get(self.url)
        self.assertEqual(len(response.json()), 2)

    def test_response_structure(self):
        """
        Verifica que la estructura de la respuesta incluye los campos esperados:
        - username
        - games_won
        - winrate
        """
        response = self.client.get(self.url)
        self.assertTrue(len(response.data) > 0)
        first = response.data[0]

        self.assertIn('username', first)
        self.assertIn('games_won', first)
        self.assertIn('winrate', first)

    def tearDown(self):
        """
        Limpia la base de datos después de cada prueba eliminando
        los jugadores, usuarios y equipos creados.
        """
        Player.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()

class IndexViewTest(TestCase):
    def setUp(self):
        Game.objects.all().delete()
        User.objects.all().delete()
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.player = Player.objects.create(user=self.user)
        self.url = reverse('web:indexView') 

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_gets_index(self):
        self.client.login(username='testuser', password='testpass')

        Game.objects.create(name='FIFA 24')
        Game.objects.create(name='Call of Duty')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/index.html')
        self.assertIn('game_list', response.context)
        self.assertEqual(len(response.context['game_list']), 2)

        expected_games = list(Game.objects.all())
        actual_games = list(response.context['game_list'])

        self.assertListEqual(actual_games, expected_games)

    def tearDown(self):
        Game.objects.all().delete()
        User.objects.all().delete()

class PrivacyPolicyViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('web:privacyPolicyView')

    def test_privacy_policy_status_and_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/privacy_policy.html')

class TermsOfUseViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('web:termsOfUseView')

    def test_terms_of_use_status_and_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

class FaqViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('web:faqView')  # Ajusta según el name definido en urls.py

    def test_faq_view_status_and_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/faq.html')

class RankingViewTest(TestCase):
    def setUp(self):
        Player.objects.all().delete()
        User.objects.all().delete()
        self.client = Client()
        self.url = reverse('web:rankingView')  # Ajusta el name en urls.py
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Crear algunos jugadores con distinto MMR
        Player.objects.create(user=self.user, mmr=150)
        Player.objects.create(user=User.objects.create_user('user2'), mmr=200)
        Player.objects.create(user=User.objects.create_user('user3'), mmr=100)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')

    def test_logged_in_user_sees_ranking(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/ranking.html')
        self.assertIn('ranking_list', response.context)

        ranking_list = response.context['ranking_list']
        # Verificar que están ordenados de mayor a menor por mmr
        mmr_values = list(ranking_list.values_list('mmr', flat=True))
        self.assertEqual(mmr_values, sorted(mmr_values, reverse=True))

    def tearDown(self):
        Player.objects.all().delete()
        User.objects.all().delete()

class TournamentListViewTest(TestCase):
    def setUp(self):
        TournamentTeam.objects.all().delete()
        Player.objects.all().delete()
        Team.objects.all().delete()
        Tournament.objects.all().delete()
        Game.objects.all().delete()
        User.objects.all().delete()
        # Usuario autenticado
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass2')
        self.client = Client()
        self.client.login(username='testuser', password='testpass')

        self.url = reverse('web:tournamentListView')  # Asegúrate que este `name` exista en urls.py

        # Juegos
        self.game1 = Game.objects.create(name='League of Legends')
        self.game2 = Game.objects.create(name='Valorant')

        # Equipos
        self.team1 = Team.objects.create(name='Alpha Team')
        self.team2 = Team.objects.create(name='Bravo Squad')

        # Jugadores (asociados a equipo)
        self.player1 = Player.objects.create(first_name='Player One', user=self.user, team=self.team1, mmr=1200)
        self.player2 = Player.objects.create(first_name='Player Two', user=self.user2, team=self.team2, mmr=1100)

        # Torneos
        self.tournament1 = Tournament.objects.create(name='LoL Open', game=self.game1, status='upcoming', start_date=timezone.now() + timedelta(days=2))
        self.tournament2 = Tournament.objects.create(name='Valorant Cup', game=self.game2, status='completed', start_date=timezone.now() + timedelta(days=2))
        self.tournament3 = Tournament.objects.create(name='LoL Finals', game=self.game1, status='upcoming', start_date=timezone.now() + timedelta(days=2))

        # Asociación equipos-torneos
        TournamentTeam.objects.create(tournament=self.tournament1, team=self.team1)
        TournamentTeam.objects.create(tournament=self.tournament2, team=self.team2)

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')

    def test_view_returns_all_tournaments_for_logged_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/tournament_list.html')
        self.assertEqual(len(response.context['tournament_list']), 3)
        self.assertIn('games', response.context)

    def test_filter_by_name(self):
        response = self.client.get(self.url, {'search': 'LoL'})
        tournament_names = [t.name for t in response.context['tournament_list']]
        self.assertTrue(all('LoL' in name for name in tournament_names))
        self.assertEqual(len(tournament_names), 2)

    def test_filter_by_game(self):
        response = self.client.get(self.url, {'game': self.game2.id})
        self.assertEqual(len(response.context['tournament_list']), 1)
        self.assertEqual(response.context['tournament_list'][0].game, self.game2)

    def test_filter_by_status(self):
        response = self.client.get(self.url, {'status': 'upcoming'})
        self.assertEqual(len(response.context['tournament_list']), 2)
        for t in response.context['tournament_list']:
            self.assertEqual(t.status, 'upcoming')

    def tearDown(self):
        TournamentTeam.objects.all().delete()
        Player.objects.all().delete()
        Team.objects.all().delete()
        Tournament.objects.all().delete()
        Game.objects.all().delete()
        User.objects.all().delete()

class SupportViewTests(TestCase):
    def setUp(self):
        User.objects.all().delete()
        self.user = User.objects.create_user(username='testuser', email='user@example.com', password='testpass')
        self.player = Player.objects.create(first_name='Player One', user=self.user)
        self.client = Client()
        self.url = reverse('web:supportView')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_view_loads_for_logged_user(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/support.html')
        self.assertIsInstance(response.context['form'], SupportForm)
        self.assertEqual(response.context['form'].initial['email'], self.user.email)

    @patch('web.views.send_mail')  # Reemplaza el import si el view está en otro módulo
    def test_successful_form_submission_sends_email(self, mock_send_mail):
        self.client.login(username='testuser', password='testpass')
        form_data = {
            'email': self.user.email,
            'subject': 'Prueba de soporte',
            'message': 'Este es un mensaje de prueba.',
        }
        response = self.client.post(self.url, form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(mock_send_mail.called)

    @patch('web.views.send_mail', side_effect=Exception("SMTP error"))
    def test_form_submission_error_shows_error_message(self, mock_send_mail):
        self.client.login(username='testuser', password='testpass')
        form_data = {
            'email': self.user.email,
            'subject': 'Error Test',
            'message': 'Mensaje que fallará al enviarse',
        }
        response = self.client.post(self.url, form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(mock_send_mail.called)

    def tearDown(self):
        User.objects.all().delete()

class UpgradeToPremiumViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user1', password='pass')
        self.player = Player.objects.create(user=self.user, role=Player.DEFAULT)
        self.url = reverse('web:upgradeToPremiumView') 

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_upgrade_role_and_redirect(self):
        self.client.login(username='user1', password='pass')
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('web:premiumView'))

        self.player.refresh_from_db()
        self.assertEqual(self.player.role, Player.PREMIUM)

    def tearDown(self):
        User.objects.all().delete()
        Player.objects.all().delete()

class TournamentCreateViewTests(TestCase):
    def setUp(self):
        User.objects.all().delete()
        Player.objects.all().delete()
        Game.objects.all().delete()
        Tournament.objects.all().delete()
        self.client = Client()
        self.user = User.objects.create_user(username='user1', password='pass', email='user1@example.com')
        self.player = Player.objects.create(user=self.user)
        self.url = reverse('web:tournamentCreateView')  # Ajusta según tu urls.py
        self.game = Game.objects.create(id=1, name='Game Test')


    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    @patch('web.views.send_mail')  # Mock para send_mail
    def test_create_tournament_success(self, mock_send_mail):
        self.client.login(username='user1', password='pass')

        data = {
            'name': 'Torneo Test',
            'start_date': timezone.now() + timedelta(days=2),
            'game': self.game.id,
            'status': "upcoming",
            'max_player_per_team': 2,
            'max_teams': 2,
            'matches_generated': False,
            'prize_pool': 1000
        }

        response = self.client.post(self.url, data)

        # Debería redirigir a la lista de torneos
        self.assertRedirects(response, reverse('web:tournamentListView'))

        tournament = Tournament.objects.get(name='Torneo Test')
        self.assertEqual(tournament.created_by, self.user)
        self.assertEqual(tournament.prize_pool, 1000)

        # Verificar que se haya llamado send_mail
        mock_send_mail.assert_called_once()

    def tearDown(self):
        User.objects.all().delete()
        Player.objects.all().delete()
        Game.objects.all().delete()
        Tournament.objects.all().delete()

