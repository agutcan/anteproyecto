from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Player, Team
from .serializers import PlayerStatsSerializer

class PlayerStatsListAPITest(APITestCase):
    def setUp(self):
        # Crear equipo y jugadores de prueba
        self.team = Team.objects.create(name="Test Team")

        self.player1 = Player.objects.create(name="Jugador Uno", team=self.team, goals=5, assists=2)
        self.player2 = Player.objects.create(name="Jugador Dos", team=self.team, goals=3, assists=4)

        self.url = reverse('playerStatsListApi')  # Ajustar al name correcto del endpoint

    def test_get_all_player_stats(self):
        response = self.client.get(self.url)
        players = Player.objects.select_related('team').all()
        serializer = PlayerStatsSerializer(players, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)

    def test_player_count(self):
        response = self.client.get(self.url)
        self.assertEqual(len(response.json()), 2)

    def test_response_structure(self):
        response = self.client.get(self.url)
        self.assertIn('name', response.data[0])
        self.assertIn('team', response.data[0])
        self.assertIn('goals', response.data[0])
      
    def tearDown(self):
    # Limpiar los objetos creados (aunque la base de datos de test se limpia por sí sola)
    Player.objects.all().delete()
    Team.objects.all().delete()

class IndexViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()
        self.url = reverse('indexView')  # Ajusta esto según el name en tu `urls.py`

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')  # Ajusta el path si usas otro login URL

    def test_logged_in_user_gets_index(self):
        self.client.login(username='testuser', password='testpass')

        Game.objects.create(name='FIFA 24')
        Game.objects.create(name='Call of Duty')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/index.html')
        self.assertIn('game_list', response.context)
        self.assertEqual(len(response.context['game_list']), 2)
        self.assertQuerysetEqual(
            response.context['game_list'],
            Game.objects.all(),
            transform=lambda x: x
        )

    def tearDown(self):
      # Limpiar los objetos creados (aunque la base de datos de test se limpia por sí sola)
      Player.objects.all().delete()
      game.objects.all().delete()




