from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.test import TestCase, Client
from rest_framework import status
from django.urls import reverse
from .models import *
from .serializers import PlayerStatsSerializer

class PlayerStatsListAPITest(APITestCase):
    def setUp(self):
        # Crear equipo de prueba
        self.team = Team.objects.create(name="Test Team")

        # Crear usuarios
        self.user1 = User.objects.create_user(username='user1', password='testpass')
        self.user2 = User.objects.create_user(username='user2', password='testpass')

        # Crear jugadores asociados a los usuarios
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
        response = self.client.get(self.url)
        players = Player.objects.select_related('team', 'user').all()
        serializer = PlayerStatsSerializer(players, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)

    def test_player_count(self):
        response = self.client.get(self.url)
        self.assertEqual(len(response.json()), 2)

    def test_response_structure(self):
        response = self.client.get(self.url)
        self.assertTrue(len(response.data) > 0)
        first = response.data[0]

        self.assertIn('user', first)
        self.assertIn('team', first)
        self.assertIn('mmr', first)
        self.assertIn('games_played', first)
        self.assertIn('games_won', first)
        self.assertIn('winrate', first)

    def tearDown(self):
        Player.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()

class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.url = reverse('web:indexView') 

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')  

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
        self.url = reverse('termsOfUseView') 

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
        self.assertTemplateUsed(response, 'web/terms_of_use.html')

class RankingViewTest(TestCase):
    def setUp(self):
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


