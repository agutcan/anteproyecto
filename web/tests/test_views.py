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
    """
    Pruebas para la vista de índice (IndexView).

    Verifica el acceso a la página principal, tanto para usuarios no autenticados
    como para usuarios autenticados, comprobando el estado HTTP y el contexto.
    """

    def setUp(self):
        """
        Prepara el entorno para las pruebas:
        - Elimina datos existentes.
        - Crea un usuario y jugador de prueba.
        - Define la URL de la vista.
        """
        Game.objects.all().delete()
        User.objects.all().delete()
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.player = Player.objects.create(user=self.user)
        self.url = reverse('web:indexView')

    def test_redirect_if_not_logged_in(self):
        """
        Comprueba que un usuario no autenticado puede acceder a la página
        de índice y recibe un status HTTP 200.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_gets_index(self):
        """
        Verifica que un usuario autenticado puede acceder a la página de índice,
        que se usa la plantilla correcta y que el contexto contiene la lista
        de juegos con la cantidad adecuada.
        """
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
        """
        Limpia los datos creados durante las pruebas.
        """
        Game.objects.all().delete()
        User.objects.all().delete()

class PrivacyPolicyViewTest(TestCase):
    """
    Pruebas para la vista de la política de privacidad.

    Verifica que la vista se carga correctamente con status HTTP 200
    y que se usa la plantilla adecuada.
    """

    def setUp(self):
        """
        Inicializa el cliente y define la URL de la vista.
        """
        self.client = Client()
        self.url = reverse('web:privacyPolicyView')

    def test_privacy_policy_status_and_template(self):
        """
        Comprueba que la vista responde con status 200
        y usa la plantilla 'privacy_policy.html'.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/privacy_policy.html')

class TermsOfUseViewTest(TestCase):
    """
    Pruebas para la vista de términos de uso.

    Verifica que la vista carga con status HTTP 200.
    """

    def setUp(self):
        """
        Inicializa el cliente y la URL para la vista.
        """
        self.client = Client()
        self.url = reverse('web:termsOfUseView')

    def test_terms_of_use_status_and_template(self):
        """
        Comprueba que la vista responde con status HTTP 200.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

class FaqViewTest(TestCase):
    """
    Pruebas para la vista de preguntas frecuentes (FAQ).

    Verifica que la vista responde correctamente y usa la plantilla esperada.
    """

    def setUp(self):
        """
        Inicializa el cliente y la URL para la vista.
        """
        self.client = Client()
        self.url = reverse('web:faqView')

    def test_faq_view_status_and_template(self):
        """
        Comprueba que la vista responde con status HTTP 200
        y que se usa la plantilla 'faq.html'.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/faq.html')

class RankingViewTest(TestCase):
    """
    Pruebas para la vista de ranking de jugadores.

    Verifica el acceso según autenticación, que el ranking esté ordenado
    correctamente y que la plantilla usada sea la esperada.
    """

    def setUp(self):
        """
        Prepara usuarios y jugadores con distintos MMR,
        limpia datos previos y define la URL de la vista.
        """
        Player.objects.all().delete()
        User.objects.all().delete()
        self.client = Client()
        self.url = reverse('web:rankingView')
        self.user = User.objects.create_user(username='testuser', password='testpass')

        Player.objects.create(user=self.user, mmr=150)
        Player.objects.create(user=User.objects.create_user('user2'), mmr=200)
        Player.objects.create(user=User.objects.create_user('user3'), mmr=100)

    def test_redirect_if_not_logged_in(self):
        """
        Verifica que un usuario no autenticado es redirigido
        al login cuando intenta acceder al ranking.
        """
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')

    def test_logged_in_user_sees_ranking(self):
        """
        Verifica que un usuario autenticado puede ver el ranking,
        que la plantilla es correcta y que la lista está ordenada por MMR descendente.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/ranking.html')
        self.assertIn('ranking_list', response.context)

        ranking_list = response.context['ranking_list']
        mmr_values = list(ranking_list.values_list('mmr', flat=True))
        self.assertEqual(mmr_values, sorted(mmr_values, reverse=True))

    def tearDown(self):
        """
        Limpia los datos creados durante las pruebas.
        """
        Player.objects.all().delete()
        User.objects.all().delete()

class TournamentListViewTest(TestCase):
    """
    Pruebas para la vista que lista los torneos.

    Verifica redirecciones según autenticación, la correcta carga de torneos,
    filtros por nombre, juego y estado, y el uso de la plantilla adecuada.
    """

    def setUp(self):
        """
        Prepara datos para los tests:
        - Limpia datos previos de torneos, equipos, jugadores, juegos y usuarios.
        - Crea usuarios, juegos, equipos, jugadores, torneos y asociaciones.
        - Autentica el cliente con un usuario.
        - Define la URL para la vista.
        """
        TournamentTeam.objects.all().delete()
        Player.objects.all().delete()
        Team.objects.all().delete()
        Tournament.objects.all().delete()
        Game.objects.all().delete()
        User.objects.all().delete()

        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass2')
        self.client = Client()
        self.client.login(username='testuser', password='testpass')

        self.url = reverse('web:tournamentListView')

        self.game1 = Game.objects.create(name='League of Legends')
        self.game2 = Game.objects.create(name='Valorant')

        self.team1 = Team.objects.create(name='Alpha Team')
        self.team2 = Team.objects.create(name='Bravo Squad')

        self.player1 = Player.objects.create(first_name='Player One', user=self.user, team=self.team1, mmr=1200)
        self.player2 = Player.objects.create(first_name='Player Two', user=self.user2, team=self.team2, mmr=1100)

        self.tournament1 = Tournament.objects.create(name='LoL Open', game=self.game1, status='upcoming', start_date=timezone.now() + timedelta(days=2))
        self.tournament2 = Tournament.objects.create(name='Valorant Cup', game=self.game2, status='completed', start_date=timezone.now() + timedelta(days=2))
        self.tournament3 = Tournament.objects.create(name='LoL Finals', game=self.game1, status='upcoming', start_date=timezone.now() + timedelta(days=2))

        TournamentTeam.objects.create(tournament=self.tournament1, team=self.team1)
        TournamentTeam.objects.create(tournament=self.tournament2, team=self.team2)

    def test_redirect_if_not_logged_in(self):
        """
        Verifica que un usuario no autenticado sea redirigido al login
        cuando intenta acceder a la lista de torneos.
        """
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')

    def test_view_returns_all_tournaments_for_logged_user(self):
        """
        Comprueba que un usuario autenticado recibe la lista completa de torneos,
        la plantilla correcta y que el contexto incluye los juegos.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/tournament_list.html')
        self.assertEqual(len(response.context['tournament_list']), 3)
        self.assertIn('games', response.context)

    def test_filter_by_name(self):
        """
        Verifica que el filtro por nombre funciona y que solo
        se devuelven torneos cuyo nombre contiene la cadena buscada.
        """
        response = self.client.get(self.url, {'search': 'LoL'})
        tournament_names = [t.name for t in response.context['tournament_list']]
        self.assertTrue(all('LoL' in name for name in tournament_names))
        self.assertEqual(len(tournament_names), 2)

    def test_filter_by_game(self):
        """
        Comprueba que el filtro por juego retorna solo torneos asociados
        al juego especificado.
        """
        response = self.client.get(self.url, {'game': self.game2.id})
        self.assertEqual(len(response.context['tournament_list']), 1)
        self.assertEqual(response.context['tournament_list'][0].game, self.game2)

    def test_filter_by_status(self):
        """
        Verifica que el filtro por estado devuelve solo torneos
        con el estado indicado.
        """
        response = self.client.get(self.url, {'status': 'upcoming'})
        self.assertEqual(len(response.context['tournament_list']), 2)
        for t in response.context['tournament_list']:
            self.assertEqual(t.status, 'upcoming')

    def tearDown(self):
        """
        Limpia todos los datos generados durante las pruebas.
        """
        TournamentTeam.objects.all().delete()
        Player.objects.all().delete()
        Team.objects.all().delete()
        Tournament.objects.all().delete()
        Game.objects.all().delete()
        User.objects.all().delete()

class SupportViewTests(TestCase):
    """
    Pruebas para la vista de soporte.

    Comprueba redirección, carga de formulario, envío de correo
    y manejo de errores en la vista de soporte.
    """

    def setUp(self):
        """
        Configura un usuario y jugador de prueba, cliente y URL.
        """
        User.objects.all().delete()
        self.user = User.objects.create_user(username='testuser', email='user@example.com', password='testpass')
        self.player = Player.objects.create(first_name='Player One', user=self.user)
        self.client = Client()
        self.url = reverse('web:supportView')

    def test_redirect_if_not_logged_in(self):
        """
        Verifica que un usuario no autenticado sea redirigido al login
        cuando intenta acceder a la vista de soporte.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_view_loads_for_logged_user(self):
        """
        Comprueba que la vista carga correctamente para un usuario autenticado,
        que la plantilla es la esperada y el formulario incluye el email inicial.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/support.html')
        self.assertIsInstance(response.context['form'], SupportForm)
        self.assertEqual(response.context['form'].initial['email'], self.user.email)

    @patch('web.views.send_mail')
    def test_successful_form_submission_sends_email(self, mock_send_mail):
        """
        Simula el envío exitoso de un formulario de soporte y verifica
        que se haya llamado a send_mail y la respuesta sea exitosa.
        """
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
        """
        Simula un error en el envío del formulario de soporte y verifica
        que la vista maneja la excepción correctamente.
        """
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
        """
        Elimina los datos de usuario creados para las pruebas.
        """
        User.objects.all().delete()

class UpgradeToPremiumViewTests(TestCase):
    """
    Pruebas para la vista de actualización a cuenta Premium.

    Verifica redirecciones y actualización del rol del jugador.
    """

    def setUp(self):
        """
        Configura usuario, jugador y cliente, y define la URL para la vista.
        """
        self.client = Client()
        self.user = User.objects.create_user(username='user1', password='pass')
        self.player = Player.objects.create(user=self.user, role=Player.DEFAULT)
        self.url = reverse('web:upgradeToPremiumView')

    def test_redirect_if_not_logged_in(self):
        """
        Verifica que un usuario no autenticado sea redirigido al login
        cuando intenta acceder a la vista de actualización.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_upgrade_role_and_redirect(self):
        """
        Verifica que un usuario autenticado cambia su rol a Premium
        y es redirigido correctamente.
        """
        self.client.login(username='user1', password='pass')
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('web:premiumView'))

        self.player.refresh_from_db()
        self.assertEqual(self.player.role, Player.PREMIUM)

    def tearDown(self):
        """
        Limpia usuarios y jugadores creados en la prueba.
        """
        User.objects.all().delete()
        Player.objects.all().delete()

class TournamentCreateViewTests(TestCase):
    """
    Pruebas para la vista de creación de torneos.

    Verifica redirecciones, creación exitosa y envío de correo.
    """

    def setUp(self):
        """
        Prepara usuario, jugador, cliente, juego y URL para la vista.
        """
        User.objects.all().delete()
        Player.objects.all().delete()
        Game.objects.all().delete()
        Tournament.objects.all().delete()

        self.client = Client()
        self.user = User.objects.create_user(username='user1', password='pass', email='user1@example.com')
        self.player = Player.objects.create(user=self.user)
        self.url = reverse('web:tournamentCreateView')
        self.game = Game.objects.create(id=1, name='Game Test')

    def test_redirect_if_not_logged_in(self):
        """
        Verifica que un usuario no autenticado sea redirigido al login
        al intentar acceder a la vista de creación de torneo.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    @patch('web.views.send_mail')
    def test_tournament_creation_and_email(self, mock_send_mail):
        """
        Simula la creación de un torneo y verifica que se guarda correctamente,
        se envía el correo y se redirige a la página de torneos.
        """
        self.client.login(username='user1', password='pass')
        form_data = {
            'name': 'New Tournament',
            'game': self.game.id,
            'status': 'upcoming',
            'start_date': '2025-12-01',
        }
        response = self.client.post(self.url, form_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Tournament.objects.filter(name='New Tournament').exists())
        self.assertTrue(mock_send_mail.called)

    def tearDown(self):
        """
        Limpia los datos creados durante la prueba.
        """
        User.objects.all().delete()
        Player.objects.all().delete()
        Game.objects.all().delete()
        Tournament.objects.all().delete()

