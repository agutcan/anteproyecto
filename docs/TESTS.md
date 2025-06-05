# ✅ Tests de Modelos (`test_models.py`)

Este archivo contiene pruebas unitarias para verificar que los modelos del sistema funcionen correctamente.

---

## ⚙️ Configuración Inicial (`setUp`)
Antes de cada test, se crean las siguientes instancias:
- Un usuario (`testuser`)
- Dos equipos (`Team One` y `Team Two`)
- Un juego (`Test Game`)
- Un torneo con fecha futura y 2 equipos permitidos (`Test Tournament`)

```python
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
```
---

## 🧪 Pruebas Incluidas

### 🎮 `test_game_creation`
Verifica que el nombre del juego se representa correctamente como string.

```python
def test_game_creation(self):
        """Verifica que el juego se crea correctamente y su representación como string es válida."""
        self.assertEqual(str(self.game), 'Test Game')
```
### 🏷️ `test_team_creation`
Verifica que el nombre del equipo se representa correctamente como string.

```python
def test_team_creation(self):
        """Verifica que el equipo se crea correctamente y su representación como string es válida."""
        self.assertEqual(str(self.team1), 'Team One')
```
### 👤 `test_player_creation`
Crea un jugador con MMR y asegura que:
- Está vinculado al equipo correcto.
- Su representación en string contiene el nombre del usuario.
```python
def test_player_creation(self):
        """Crea un jugador y valida su asociación al equipo y su representación textual."""
        player = Player.objects.create(user=self.user, team=self.team1, mmr=100)
        self.assertEqual(player.team.name, 'Team One')
        self.assertIn('testuser', str(player))
```
### 🏆 `test_tournament_creation`
Verifica la creación y representación textual del torneo.
```python
def test_tournament_creation(self):
        """Verifica que el torneo se crea correctamente y su estado inicial es 'Upcoming'."""
        self.assertEqual(self.tournament.name, 'Test Tournament')
        self.assertEqual(str(self.tournament), 'Test Tournament (Upcoming)')

```
### 🚫 `test_tournament_team_unique`
Comprueba que no se puede registrar el mismo equipo dos veces en el mismo torneo (restricción `unique_together`).
```python
def test_tournament_team_unique(self):
        """
        Verifica que un equipo no puede inscribirse dos veces en el mismo torneo.
        Espera una excepción por la restricción de unicidad.
        """
        TournamentTeam.objects.create(tournament=self.tournament, team=self.team1)
        with self.assertRaises(Exception):
            TournamentTeam.objects.create(tournament=self.tournament, team=self.team1)
```
### ⚔️ `test_match_creation`
Crea un partido entre dos equipos y verifica que su representación en string incluye "Partido".
```python
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
```
### 🧾 `test_match_result_creation`
Crea un resultado de partido, verifica:
- El equipo ganador.
- Que su string incluye "Resultado:".
```python
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
```
### 📜 `test_match_log_creation`
Crea un log de partido con un evento y verifica que dicho evento se representa correctamente.
```python
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
```
### 🎁 `test_reward_creation`
Crea una recompensa y verifica su representación como `"Nombre (X coins)"`.
```python
def test_reward_creation(self):
        """Crea una recompensa y verifica su representación textual con nombre y coste en monedas."""
        reward = Reward.objects.create(name="Camisa", coins_cost=300, stock=10)
        self.assertEqual(str(reward), "Camisa (300 coins)")
```
### 💸 `test_redemption_creation`
Verifica que el canje de una recompensa por parte de un usuario se representa como: `"username redeemed recompensa"`.
```python
def test_redemption_creation(self):
        """Verifica que una redención de recompensa por un usuario se representa correctamente."""
        reward = Reward.objects.create(name="Gorra", coins_cost=100, stock=5)
        redemption = Redemption.objects.create(user=self.user, reward=reward)
        self.assertIn("testuser redeemed Gorra", str(redemption))
```
---

## 🧹 Limpieza (`tearDown`)
Después de cada test, se eliminan todas las instancias creadas para evitar interferencias entre pruebas.
```python
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
```
---

# ✅ Tests de Vistas (`test_views.py`)

Este archivo contiene pruebas para validar el comportamiento de las distintas vistas del sistema. Se asegura que las vistas devuelvan los templates correctos, realicen redirecciones apropiadas, y manejen correctamente los datos del contexto y los formularios.

---

## 📊 `PlayerStatsListAPITest`

Pruebas para la vista API que devuelve estadísticas de jugadores en formato JSON.

### ⚙️ Configuración Inicial (`setUp`)

* Crea un equipo de prueba.
* Crea dos jugadores con estadísticas distintas.
* Define la URL de la vista a probar.

### 🧪 Pruebas Incluidas

* `test_get_all_player_stats`: Verifica que se devuelvan los datos correctos.
* `test_player_count`: Verifica que se devuelvan 2 jugadores.
* `test_response_structure`: Asegura la estructura del JSON (`username`, `games_won`, `winrate`).

```python
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
```

---

## 🏠 `IndexViewTest`

Pruebas para la vista principal del sitio.

### ⚙️ Configuración Inicial

* Crea un usuario y un jugador.
* Define la URL de la vista de inicio.

### 🧪 Pruebas Incluidas

* `test_redirect_if_not_logged_in`: Asegura acceso sin login (status 200).
* `test_logged_in_user_gets_index`: Verifica que se rendericen los juegos correctamente en el contexto.

```python
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
```

---

## 🔒 `PrivacyPolicyViewTest`

Pruebas para la vista de política de privacidad.

### 🧪 Pruebas Incluidas

* `test_privacy_policy_status_and_template`: Asegura que carga el template correcto con status 200.

```python
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
```

---

## 📜 `TermsOfUseViewTest`

Pruebas para la vista de términos de uso.

### 🧪 Pruebas Incluidas

* `test_terms_of_use_status_and_template`: Verifica que la vista se renderice correctamente.

```python
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
```

---

## ❓ `FaqViewTest`

Pruebas para la vista de preguntas frecuentes.

### 🧪 Pruebas Incluidas

* `test_faq_view_status_and_template`: Verifica status 200 y uso del template `faq.html`.

```python
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
```

---

## 🏆 `RankingViewTest`

Pruebas para la vista del ranking de jugadores ordenados por MMR.

### ⚙️ Configuración Inicial

* Crea 3 jugadores con diferentes MMR.

### 🧪 Pruebas Incluidas

* `test_redirect_if_not_logged_in`: Redirecciona si no está logueado.
* `test_logged_in_user_sees_ranking`: Verifica orden descendente por MMR.

```python
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
```

---

## 📅 `TournamentListViewTest`

Pruebas para la lista de torneos, con filtros por nombre, juego o estado.

### ⚙️ Configuración Inicial

* Crea juegos, equipos, jugadores y torneos asociados.

### 🧪 Pruebas Incluidas

* `test_redirect_if_not_logged_in`: Redirecciona si no está logueado.
* `test_view_returns_all_tournaments_for_logged_user`: Devuelve todos los torneos.
* `test_filter_by_name`: Filtra por nombre de torneo.
* `test_filter_by_game`: Filtra por ID de juego.
* `test_filter_by_status`: Filtra por estado (ej. `upcoming`).

```python
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
```

---

## 📬 `SupportViewTests`

Pruebas para la vista de soporte y envío de correo.

### ⚙️ Configuración Inicial

* Crea un usuario y su jugador asociado.

### 🧪 Pruebas Incluidas

* `test_redirect_if_not_logged_in`: Redirecciona a login.
* `test_view_loads_for_logged_user`: Muestra el formulario con el email prellenado.
* `test_successful_form_submission_sends_email`: Envía email correctamente.
* `test_form_submission_error_shows_error_message`: Maneja errores en el envío.

```python
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
```

---

## 💎 `UpgradeToPremiumViewTests`

Pruebas para la vista de mejora de cuenta a premium.

### ⚙️ Configuración Inicial

* Crea un usuario estándar.

### 🧪 Pruebas Incluidas

* `test_redirect_if_not_logged_in`: Redirecciona si no está autenticado.
* `test_upgrade_role_and_redirect`: Cambia el rol a premium y redirige.

```python
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
```

---

## 🏗️ `TournamentCreateViewTests`

Pruebas para la creación de torneos por usuarios autenticados.

### ⚙️ Configuración Inicial

* Crea un usuario, su jugador, un juego y define la URL.

### 🧪 Pruebas Incluidas

* `test_redirect_if_not_logged_in`: Redirecciona si no está autenticado.
* `test_create_tournament_success`: Crea correctamente el torneo y envía email de confirmación.

```python
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
```

---

> 🧼 Todas las clases de test para las vistas cuentan con un método `tearDown` para limpiar los datos creados en la base de pruebas.


## 🔄 Navegación
- ️🏗️ [Estructura del Proyecto y esquema de base de datos](PROJECT_STRUCTURE.md)
- ⚙️ [Admin](ADMIN.md)
- 🖼️ [Vistas](VIEWS.md)
- ⏰ [Tareas programadas](TASKS.md)
- 🧩 [Modelos](MODELS.md)
- 📝 [Formularios](FORMS.md)
- ✅ [Test](TESTS.md)
- 🔄 [Serializadores](SERIALIZERS.md)
- 🧠 [Funciones](FUNCTIONS.md)
- ⬅️ [Volver al README principal](../README.md)