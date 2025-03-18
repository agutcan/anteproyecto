# Generated by Django 5.1.7 on 2025-03-18 12:19

from django.db import migrations

# Función que elimina todos los datos de la base de datos de la aplicación
from django.db import migrations

def eliminar_datos(apps, schema_editor):
    # Obtener los modelos de la aplicación 'web'
    Game = apps.get_model('web', 'Game')
    Tournament = apps.get_model('web', 'Tournament')
    Team = apps.get_model('web', 'Team')
    Player = apps.get_model('web', 'Player')
    Match = apps.get_model('web', 'Match')
    MatchResult = apps.get_model('web', 'MatchResult')
    TournamentTeam = apps.get_model('web', 'TournamentTeam')
    MatchLog = apps.get_model('web', 'MatchLog')
    User = apps.get_model('auth', 'User')  # Modelo User de Django

    # Eliminar registros de log de partidos
    MatchLog.objects.all().delete()
    # Eliminar los resultados de los partidos
    MatchResult.objects.all().delete()
    # Eliminar los partidos
    Match.objects.all().delete()
    # Eliminar equipos de los torneos
    TournamentTeam.objects.all().delete()
    # Eliminar los torneos
    Tournament.objects.all().delete()
    # Eliminar los jugadores
    Player.objects.all().delete()
    # Eliminar los equipos
    Team.objects.all().delete()
    # Eliminar los juegos
    Game.objects.all().delete()
    # Eliminar los usuarios
    User.objects.all().delete()

# Función que pobla la base de datos con datos de prueba
def poblar_datos(apps, schema_editor):
    # Obtener los modelos de la aplicación 'web'
    Game = apps.get_model('web', 'Game')
    Tournament = apps.get_model('web', 'Tournament')
    Team = apps.get_model('web', 'Team')
    Player = apps.get_model('web', 'Player')
    Match = apps.get_model('web', 'Match')
    MatchResult = apps.get_model('web', 'MatchResult')
    TournamentTeam = apps.get_model('web', 'TournamentTeam')
    User = apps.get_model('auth', 'User')  # Modelo User de Django
    MatchLog = apps.get_model('web', 'MatchLog')  # Modelo para los logs

    # Función para crear registros de eventos en el log
    def log_event(match, team, player, event):
        """Función para crear un log de eventos en la partida."""
        log = MatchLog(
            match=match,
            team=team,
            player=player,
            event=event
        )
        log.save()  # Guarda el log en la base de datos

    # Crear usuarios
    users = [
        User(username="player1", password="password1", first_name="John", last_name="Doe", email="john@example.com"),
        User(username="player2", password="password2", first_name="Jane", last_name="Doe", email="jane@example.com"),
        User(username="player3", password="password3", first_name="Alice", last_name="Smith", email="alice@example.com"),
        User(username="player4", password="password4", first_name="Bob", last_name="Johnson", email="bob@example.com"),
    ]
    User.objects.bulk_create(users)  # Crear todos los usuarios de una vez

    # Crear juegos
    games = [
        Game(name="Valorant", genre="Shooter táctico"),
        Game(name="League of Legends", genre="MOBA"),
        Game(name="Counter-Strike 2", genre="Shooter táctico")
    ]
    Game.objects.bulk_create(games)  # Guardar todos los juegos de una vez

    # Crear equipos
    teams = [
        Team(name="Los Guerreros del Sol"),
        Team(name="La Legión Oscura"),
        Team(name="Los Centinelas del Reino"),
        Team(name="Héroes de la Alianza")
    ]
    Team.objects.bulk_create(teams)  # Guardar todos los equipos de una vez

    # Crear jugadores
    players = [
        Player(user=users[0], team=teams[0], role='Capitán', games_played=100, games_won=70),
        Player(user=users[1], team=teams[1], role='Miembro', games_played=80, games_won=50),
        Player(user=users[2], team=teams[2], role='Capitán', games_played=120, games_won=90),
        Player(user=users[3], team=teams[3], role='Miembro', games_played=90, games_won=65)
    ]
    Player.objects.bulk_create(players)  # Guardar todos los jugadores de una vez

    # Llamar a update_winrate() para cada jugador creado y registrar el log
    for player in players:
        player.winrate = (player.games_won / player.games_played) * 100 if player.games_played > 0 else 0
        player.save()
        log_event(None, player.team, player, f"Winrate actualizado: {player.winrate:.2f}%")  # Registrar evento de actualización

    # Crear torneos
    tournaments = [
        Tournament(name="Torneo Internacional de Valorant", game=games[0], start_date="2025-04-01", end_date="2025-04-30", status="upcoming", prize_pool=5000.00, created_by=users[0]),
        Tournament(name="Campeonato Mundial de League of Legends", game=games[1], start_date="2025-05-01", end_date="2025-05-15", status="upcoming", prize_pool=10000.00, created_by=users[1])
    ]
    Tournament.objects.bulk_create(tournaments)  # Guardar todos los torneos de una vez

    # Asignar equipos a torneos
    tournament_teams = [
        TournamentTeam(tournament=tournaments[0], team=teams[0], seed=1),
        TournamentTeam(tournament=tournaments[0], team=teams[1], seed=2),
        TournamentTeam(tournament=tournaments[1], team=teams[2], seed=1),
        TournamentTeam(tournament=tournaments[1], team=teams[3], seed=2)
    ]
    TournamentTeam.objects.bulk_create(tournament_teams)  # Guardar todos los equipos en los torneos

    # Crear partidos entre equipos
    matches = [
        Match(tournament=tournaments[0], round=1, team1=teams[0], team2=teams[1], scheduled_at="2025-04-05T10:00:00", status="pending"),
        Match(tournament=tournaments[1], round=1, team1=teams[2], team2=teams[3], scheduled_at="2025-05-02T10:00:00", status="pending")
    ]
    Match.objects.bulk_create(matches)  # Guardar todos los partidos de una vez

    # Crear resultados de partidos (ejemplo)
    match_results = [
        MatchResult(match=matches[0], winner=teams[0], team1_score=2, team2_score=1),
        MatchResult(match=matches[1], winner=teams[2], team1_score=3, team2_score=0)
    ]
    MatchResult.objects.bulk_create(match_results)  # Guardar todos los resultados de los partidos

    # Crear logs para los partidos
    log_event(matches[0], teams[0], None, "Partido programado: 2-1 vs Los Guerreros del Sol vs La Legión Oscura")
    log_event(matches[1], teams[2], None, "Partido programado: 3-0 vs Los Centinelas del Reino vs Héroes de la Alianza")

    # Creación de usuarios para la administración
    User.objects.create_user(username='prueba', password='prueba')  # Crear un usuario normal
    User.objects.create_superuser(username='admin', email='admin@example.com', password='admin')  # Crear un superusuario


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_alter_matchlog_match_alter_matchlog_player_and_more'),
    ]

    # Operaciones que se ejecutan: poblar los datos y definir cómo eliminarlos
    operations = [
        migrations.RunPython(poblar_datos, reverse_code=eliminar_datos),  # Función para poblar y eliminar datos
    ]
