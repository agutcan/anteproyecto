# Generated by Django 5.1.7 on 2025-03-18 12:19

from django.db import migrations

# Función que elimina todos los datos de la base de datos de la aplicación
from django.db import migrations
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django_celery_beat.models import PeriodicTask, IntervalSchedule

import json

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
    Reward = apps.get_model('web', 'Reward')
    Redemption = apps.get_model('web', 'Redemption')

    # Eliminar tareas periódicas
    PeriodicTask.objects.all().delete()
    # Eliminar intervalos
    IntervalSchedule.objects.all().delete()
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
    # Eliminar las recomponsas
    Reward.objects.all().delete()
    # Eliminar las reclamaciones
    Redemption.objects.all().delete()

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
    Reward = apps.get_model('web', 'Reward')
    Redemption = apps.get_model('web', 'Redemption')

    # Crear usuarios
    users = [
        User(username="player8", password="Usuario1", first_name="Leo", last_name="Doe", email="Leo@example.com"),
        User(username="player9", password="Usuario1", first_name="Clara", last_name="Lee", email="clara@example.com"),
        User(username="player10", password="Usuario1", first_name="Liam", last_name="Kim", email="liam@example.com"),
        User(username="player11", password="Usuario1", first_name="Olivia", last_name="Chen",
             email="olivia@example.com"),
        User(username="player12", password="Usuario1", first_name="Noah", last_name="Wang", email="noah@example.com"),
        User(username="player13", password="Usuario1", first_name="Emma", last_name="Park", email="emma@example.com"),
        User(username="player14", password="Usuario1", first_name="Mason", last_name="Nguyen",
             email="mason@example.com"),
        User(username="player15", password="Usuario1", first_name="Sophia", last_name="Tran",
             email="sophia@example.com"),
        User(username="player16", password="Usuario1", first_name="James", last_name="Lopez",
             email="james@example.com"),
        User(username="player17", password="Usuario1", first_name="Ava", last_name="Garcia", email="ava@example.com"),
        User(username="player18", password="Usuario1", first_name="Lucas", last_name="Martinez",
             email="lucas@example.com"),
        User(username="player19", password="Usuario1", first_name="Mia", last_name="Hernandez",
             email="mia@example.com"),
        User(username="player20", password="Usuario1", first_name="Benjamin", last_name="Ramirez",
             email="benjamin@example.com"),
        User(username="player21", password="Usuario1", first_name="Amelia", last_name="Torres",
             email="amelia@example.com"),
        User(username="player22", password="Usuario1", first_name="Logan", last_name="Rivera",
             email="logan@example.com"),
        User(username="player23", password="Usuario1", first_name="Evelyn", last_name="Gomez",
             email="evelyn@example.com"),
        User(username="player24", password="Usuario1", first_name="Elijah", last_name="Sanchez",
             email="elijah@example.com"),
        User(username="player25", password="Usuario1", first_name="Harper", last_name="Reyes",
             email="harper@example.com"),
        User(username="player26", password="Usuario1", first_name="Daniel", last_name="Flores",
             email="daniel@example.com"),
        User(username="player27", password="Usuario1", first_name="Daniel", last_name="Flores",
             email="daniel4@example.com"),
        User(username="player28", password="Usuario1", first_name="Daniel", last_name="Flores",
             email="daniel2@example.com"),
        User(username="player29", password="Usuario1", first_name="Daniel", last_name="Flores",
             email="daniel23@example.com"),

    ]
    User.objects.bulk_create(users)  # Crear todos los usuarios de una vez

    # Crear juegos
    games = [
        Game(name="Valorant", genre="Shooter táctico", image="games/valorant.webp"),
        Game(name="League of Legends", genre="MOBA", image="games/lol.webp"),
        Game(name="Counter-Strike 2", genre="Shooter táctico", image="games/cs2.webp"),
    ]
    Game.objects.bulk_create(games)  # Guardar todos los juegos de una vez

    # Crear jugadores
    players = [
        Player(user=users[0], games_played=40, games_won=20, mmr=75, renombre=30, coins=800),
        Player(user=users[1], country='CL', games_played=60, games_won=35, role='Premium', coins=1500),
        Player(user=users[2], games_played=70, games_won=50, mmr=85),
        Player(user=users[3], country='UY', games_played=55, games_won=25, renombre=60),
        Player(user=users[4], games_played=30, games_won=15),
        Player(user=users[5], games_played=100, games_won=80, coins=2500),
        Player(user=users[6], country='AR', games_played=85, games_won=55, mmr=95, role='Premium'),
        Player(user=users[7], country='BR', games_played=75, games_won=40, coins=1200),
        Player(user=users[8], games_played=20, games_won=10, renombre=15),
        Player(user=users[9], games_played=45, games_won=30, mmr=60, coins=700),
        Player(user=users[10], country='PE', games_played=90, games_won=60, role='Premium'),
        Player(user=users[11], games_played=80, games_won=50, coins=1800),
        Player(user=users[12], games_played=35, games_won=20),
        Player(user=users[13], games_played=55, games_won=35, renombre=45, coins=950),
        Player(user=users[14], country='AR', games_played=65, games_won=45),
        Player(user=users[15], country='BR', games_played=75, games_won=60, mmr=88, role='Premium'),
        Player(user=users[16], games_played=25, games_won=10, renombre=20),
        Player(user=users[17], games_played=95, games_won=70, coins=2300),
        Player(user=users[18], games_played=95, games_won=70, coins=2300),
        Player(user=users[19], games_played=95, mmr=85, games_won=70, coins=2300),
        Player(user=users[20], games_played=95, games_won=70, coins=2300),
        Player(user=users[21], games_played=95, mmr=85,games_won=70, coins=2300),
    ]
    Player.objects.bulk_create(players)  # Guardar todos los jugadores de una vez

    # Crear equipos
    teams = [
        Team(name="Dragones de Fuego"),
        Team(name="Guardianes del Abismo"),
        Team(name="Titanes del Coloso"),
        Team(name="Espadas de Acero"),
        Team(name="Vikings del Trueno"),
        Team(name="Los Inmortales"),
        Team(name="Cuervos de la Noche"),
        Team(name="Reyes de la Tormenta"),
        Team(name="Ángeles del Juicio"),
        Team(name="Berserkers del Caos"),
        Team(name="Lobos de la Luna"),
        Team(name="Ejército del Fénix"),
        Team(name="Escorpiones Venenosos"),
        Team(name="Revolucionarios del Desierto"),
        Team(name="Fuerzas de la Luz"),
        Team(name="Luchadores del Viento"),
        Team(name="Furiosos Guerreros"),
        Team(name="Cazadores del Vacío"),
        Team(name="Legión de Hierro"),
        Team(name="Legión de Madera"),
        Team(name="Legión de Plata"),
        Team(name="Legión de Bronce"),
        Team(name="Legión de Plastico"),
    ]
    Team.objects.bulk_create(teams)  # Guardar todos los equipos de una vez

    contador = 0
    for player in players:
        player.team = teams[contador]
        contador+=1
        player.save()

    contador = 0
    for team in teams:
        team.leader = team.player_set.first()
        team.save()

    # Crear torneos
    tournaments = [
        Tournament(name="4 teams 2 teams inactive", game=games[1],  max_player_per_team=1, max_teams=4, start_date = timezone.now() + timedelta(minutes=1), prize_pool=1000.00, created_by=users[0]),
        Tournament(name="4 teams 4 teams inactive", game=games[1],  max_player_per_team=1, max_teams=4, start_date = timezone.now() + timedelta(minutes=1), prize_pool=1000.00, created_by=users[0]),
        Tournament(name="8 teams 4 teams inactive", game=games[1],  max_player_per_team=1, max_teams=8, start_date = timezone.now() + timedelta(minutes=1), prize_pool=1000.00, created_by=users[0]),
        Tournament(name="8 teams 8 teams inactive", game=games[1],  max_player_per_team=1, max_teams=8, start_date = timezone.now() + timedelta(minutes=1), prize_pool=1000.00, created_by=users[0]),
        Tournament(name="4 teams 4 teams", game=games[1],  max_player_per_team=1, max_teams=4, start_date = timezone.now() + timedelta(minutes=1), prize_pool=1000.00, created_by=users[0]),
    ]
    Tournament.objects.bulk_create(tournaments)  # Guardar todos los torneos de una vez

    # Asignar equipos a torneos
    tournament_teams = [
        TournamentTeam(tournament=tournaments[0], team=teams[0]),
        TournamentTeam(tournament=tournaments[0], team=teams[1]),
        TournamentTeam(tournament=tournaments[1], team=teams[2]),
        TournamentTeam(tournament=tournaments[1], team=teams[3]),
        TournamentTeam(tournament=tournaments[1], team=teams[4]),
        TournamentTeam(tournament=tournaments[1], team=teams[5]),
        TournamentTeam(tournament=tournaments[2], team=teams[6]),
        TournamentTeam(tournament=tournaments[2], team=teams[7]),
        TournamentTeam(tournament=tournaments[2], team=teams[8]),
        TournamentTeam(tournament=tournaments[2], team=teams[9]),
        TournamentTeam(tournament=tournaments[3], team=teams[10]),
        TournamentTeam(tournament=tournaments[3], team=teams[11]),
        TournamentTeam(tournament=tournaments[3], team=teams[12]),
        TournamentTeam(tournament=tournaments[3], team=teams[13]),
        TournamentTeam(tournament=tournaments[3], team=teams[14]),
        TournamentTeam(tournament=tournaments[3], team=teams[15]),
        TournamentTeam(tournament=tournaments[3], team=teams[16]),
        TournamentTeam(tournament=tournaments[3], team=teams[17]),
        TournamentTeam(tournament=tournaments[4], team=teams[18]),
        TournamentTeam(tournament=tournaments[4], team=teams[19]),
        TournamentTeam(tournament=tournaments[4], team=teams[20]),
        TournamentTeam(tournament=tournaments[4], team=teams[21]),
    ]
    TournamentTeam.objects.bulk_create(tournament_teams)  # Guardar todos los equipos en los torneos

    # Crear recompensas
    rewards = [
        Reward(name="Premium Skin", description="Una skin exclusiva para valorant.",
               coins_cost=500, stock=100, is_active=True,
               created_at=timezone.now(), updated_at=timezone.now(), image="rewards/skin.webp"),
        Reward(name="Double XP Boost", description="Duplica tu experiencia ganada en partidas durante 24 horas.",
               coins_cost=300, stock=50, is_active=True,
               created_at=timezone.now(), updated_at=timezone.now(), image="rewards/x2.webp"),
        Reward(name="VIP Access", description="Accede a eventos VIP exclusivos dentro de la página.",
               coins_cost=1000, stock=20, is_active=True,
               created_at=timezone.now(), updated_at=timezone.now(), image="rewards/vip.webp"),
    ]

    # Usar bulk_create para insertar las recompensas de forma eficiente
    Reward.objects.bulk_create(rewards)

    redemptions = [
        Redemption(user=users[0], reward=rewards[0], redeemed_at=timezone.now()),
        Redemption(user=users[1], reward=rewards[1], redeemed_at=timezone.now()),
        Redemption(user=users[2], reward=rewards[2], redeemed_at=timezone.now())
    ]

    # Usar bulk_create para insertar las redenciones de forma eficiente
    Redemption.objects.bulk_create(redemptions)

    # Creación de usuarios para la administración
    User.objects.create_user(username='prueba', password='prueba')  # Crear un usuario normal
    User.objects.create_superuser(username='admin', email='admin@example.com', password='admin')  # Crear un superusuario

    players = [
        Player(user=get_object_or_404(User, username="prueba")),
        Player(user=get_object_or_404(User, username="admin")),
    ]
    Player.objects.bulk_create(players)  # Guardar todos los jugadores de una vez

    # Crear o recuperar el intervalo de 10 segundos
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=10,
        period=IntervalSchedule.SECONDS,
    )

    # Nombre de la tarea (coincide con la función @shared_task)
    task_name = 'web.tasks.update_tournament_status'

    PeriodicTask.objects.create(
        interval=schedule,
        name='Actualizar estado de torneos cada 10 segundos',
        task=task_name,
        args=json.dumps([]),  # Argumentos si tu tarea los necesita
    )
    print(f"Tarea periódica '{task_name}' creada correctamente.")


    # Nombre de la tarea (coincide con la función @shared_task)
    task_name = 'web.tasks.check_teams_ready_for_match'

    # Crear la tarea periódica si no existe
    PeriodicTask.objects.create(
        interval=schedule,
        name='Comprobar si equipos están listos cada 10 segundos',
        task=task_name,
        args=json.dumps([]),
    )
    print(f"Tarea periódica '{task_name}' creada correctamente.")


    # Nombre de la tarea (coincide con la función @shared_task)
    task_name = 'web.tasks.check_tournament_match_progress'

    PeriodicTask.objects.create(
        interval=schedule,
        name='Verificar progreso de torneos cada 10 segundos',
        task=task_name,
        args=json.dumps([]),
    )
    print(f"Tarea periódica '{task_name}' creada correctamente.")


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0019_team_searching_teammates_alter_team_leader'),
    ]

    # Operaciones que se ejecutan: poblar los datos y definir cómo eliminarlos
    operations = [
        migrations.RunPython(poblar_datos, reverse_code=eliminar_datos),  # Función para poblar y eliminar datos
    ]

