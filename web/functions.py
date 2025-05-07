from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from .models import *
from django.db import transaction
from itertools import zip_longest

def update_players_stats(team, is_winner=False):
    """
    Actualiza las estadísticas de los jugadores de un equipo después de un partido.

    Modifica los campos `games_played`, `games_won`, `winrate`, `mmr` y `renombre` según
    si el equipo ganó o no el partido.

    Argumentos:
    team (Team): El equipo cuyos jugadores serán actualizados.
    is_winner (bool): Indica si el equipo ganó el partido. Es opcional
    """    
    # Recorre todos los jugadores del equipo
    for player in team.player_set.all():
        
        # Incrementa el contador de juegos jugados para cada jugador
        player.games_played += 1
        
        # Si el equipo ganó el partido, incrementa los juegos ganados
        if is_winner:
            player.games_won += 1
        
        # Actualiza el winrate del jugador
        player.update_winrate()

        # Actualiza el MMR del jugador. Si el jugador ganó, aumenta su MMR en 10, 
        # de lo contrario lo disminuye en 5, pero no puede bajar de 10
        if is_winner:
            player.mmr += 10
        else:
            player.mmr = max(10, player.mmr - 5)

        # Si el jugador ganó, incrementa su renombre en 5 unidades
        if is_winner:
            increase_player_renombre(player, amount=5, reason="Victoria en partido oficial")
        
        # Guarda los cambios realizados en el jugador
        player.save()



def generate_matches_by_mmr(tournament_id, round=1, tournament_teams=None):
    """
    Genera los partidos del torneo basados en el MMR de los equipos.
    
    Argumentos:
    tournament_id (int): El ID del torneo para el cual se generarán los partidos.
    round (int): El número de la ronda actual del torneo.
    tournament_teams (QuerySet): Lista de equipos que participan en el torneo (opcional).
    """
    
    # Obtener el torneo utilizando el ID proporcionado
    tournament = Tournament.objects.get(id=tournament_id)

    # Verificar el número de equipos en el torneo
    if not tournament_teams:
        # Si no se pasan equipos, los obtenemos desde la base de datos
        tournament_teams = TournamentTeam.objects.filter(tournament=tournament).select_related('team')
    
    # Número total de equipos en el torneo
    num_teams = tournament_teams.count()

    # Si el número de equipos es impar o 0, cancelamos el torneo
    if num_teams == 0 or num_teams % 2 != 0:
        # Enviar correo a todos los jugadores del torneo notificando la cancelación
        players = Player.objects.filter(team__tournamentteam__tournament=tournament).select_related('tournament')
        for player in players:
            send_mail(
                'Torneo Cancelado',  # Asunto del correo
                f'Hola {player.user.username},\n\nLamentablemente, el torneo {tournament.name} ha sido cancelado debido a un número impar de equipos.',
                'administracion@arenagg.com',  # Remitente (asegúrate de configurar un remitente válido)
                [player.user.email],  # Correo del jugador
                fail_silently=False,  # Si ocurre un error, lanzar una excepción
            )

        # Eliminar el torneo cancelado
        tournament.delete()
        print(f"⚠️ El torneo {tournament.name} ha sido cancelado debido a un número impar de equipos.")
        return

    # Si el número de equipos es par, procedemos a generar los partidos
    team_mmr_pairs = []
    for tt in tournament_teams:
        # Obtener el MMR promedio del equipo
        avg_mmr = tt.team.get_avg_mmr()  # Se asume que 'get_avg_mmr' devuelve el MMR promedio del equipo
        team_mmr_pairs.append((tt, avg_mmr))

    # Ordenar los equipos por su MMR (de menor a mayor)
    team_mmr_pairs.sort(key=lambda x: x[1])

    # Emparejar los equipos basados en el MMR, haciendo parejas entre los equipos
    pairings = list(zip_longest(team_mmr_pairs[::2], team_mmr_pairs[1::2]))

    # Crear los partidos en la base de datos
    for pair in pairings:
        if pair[0] and pair[1]:
            team1 = pair[0][0]  # Primer equipo de la pareja
            team2 = pair[1][0]  # Segundo equipo de la pareja
            Match.objects.create(
                tournament=tournament,
                round=round,
                scheduled_at=timezone.now() + timezone.timedelta(minutes=5),  # Programar el partido para dentro de 5 minutos
                team1=team1.team,  # Asignar el primer equipo
                team2=team2.team,  # Asignar el segundo equipo
            )

    # Marcar que los partidos han sido generados y guardar el estado del torneo
    tournament.matches_generated = True
    tournament.save()



def record_match_result(match, winner, team1_score, team2_score):
    """
    Registra el resultado de un partido, actualiza el estado del partido a 'completed' 
    y envía correos electrónicos de confirmación a los jugadores de ambos equipos.
    
    Argumentos:
    match (Match): El partido cuyo resultado se está registrando.
    winner (Team): El equipo que ganó el partido.
    team1_score (int): El marcador del primer equipo.
    team2_score (int): El marcador del segundo equipo.
    """
    
    # Registrar el resultado del partido en la base de datos
    result = MatchResult.objects.create(
        match=match,  # Relacionar con el partido
        winner=winner,  # Registrar al equipo ganador
        team1_score=team1_score,  # Registrar la puntuación del primer equipo
        team2_score=team2_score  # Registrar la puntuación del segundo equipo
    )

    # Actualizar el estado del partido a 'completed' (finalizado)
    match.status = 'completed'
    match.save()  # Guardar el estado actualizado del partido

    # Enviar correos electrónicos a los jugadores del equipo 1
    for player in match.team1.player_set.all():
        send_mail(
            subject='✅ ¡Partida finalizada!',  # Asunto del correo
            message=(
                f'Hola {player.user.username},\n\n'  # Saludo al jugador
                'La partida ha finalizado correctamente.\n\n'
                f'Resultado del partido {match}: {team1_score}-{team2_score}\n\n'  # Resultado del partido
                '- El equipo de ArenaGG'  # Firma
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,  # Remitente configurado en settings
            recipient_list=[player.user.email],  # Lista de destinatarios (correo del jugador)
            fail_silently=False,  # Si ocurre un error, se lanza una excepción
        )

    # Enviar correos electrónicos a los jugadores del equipo 2
    for player in match.team2.player_set.all():
        send_mail(
            subject='✅ ¡Partida finalizada!',  # Asunto del correo
            message=(
                f'Hola {player.user.username},\n\n'  # Saludo al jugador
                'La partida ha finalizado correctamente.\n\n'
                f'Resultado del partido {match}: {team1_score}-{team2_score}\n\n'  # Resultado del partido
                '- El equipo de ArenaGG'  # Firma
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,  # Remitente configurado en settings
            recipient_list=[player.user.email],  # Lista de destinatarios (correo del jugador)
            fail_silently=False,  # Si ocurre un error, se lanza una excepción
        )

    # Imprimir el resultado registrado en la consola para verificar
    print(f"Resultado registrado para el partido {match}: {team1_score}-{team2_score}")


def create_match_log(match, event, team=None, player=None):
    """
    Crea un registro (log) de evento en una partida.

    Args:
        match (Match): Instancia del partido.
        event (str): Descripción del evento.
        team (Team, optional): Instancia del equipo relacionado al evento.
        player (Player, optional): Instancia del jugador relacionado al evento.

    Returns:
        MatchLog: El registro creado.
    """
    log = MatchLog.objects.create(
        match=match,
        event=event,
        team=team,
        player=player
    )
    print(f"Log creado para el partido {match}: {event}")
    return log

def decrease_player_renombre(player, amount, reason=None):
    """
    Disminuye el renombre de un jugador y crea un log del evento,
    salvo que ya tenga 1 o menos de renombre.

    Args:
        player (Player): Instancia del jugador.
        amount (int): Cantidad de renombre a disminuir.
        reason (str, optional): Razón del castigo o pérdida de renombre.

    Returns:
        Player: El jugador actualizado (o sin cambios si no se aplicó reducción).
    """

    original_renombre = player.renombre
    player.renombre = max(1, player.renombre - amount)
    player.save()

    # Crear log asociado si se proporciona razón
    if reason and hasattr(player, 'match_set'):
        last_match = player.match_set.order_by('-scheduled_at').first()
        if last_match:
            create_match_log(
                match=last_match,
                event=f"Renombre reducido en {amount} por: {reason}",
                player=player
            )

    print(f"Renombre reducido para {player}: {original_renombre} → {player.renombre}")
    return player

def increase_player_renombre(player, amount, reason=None):
    """
    Aumenta el renombre de un jugador y crea un log del evento,
    salvo que ya tenga 100 o más de renombre.

    Args:
        player (Player): Instancia del jugador.
        amount (int): Cantidad de renombre a aumentar.
        reason (str, optional): Razón del reconocimiento o aumento de renombre.

    Returns:
        Player: El jugador actualizado (o sin cambios si no se aplicó aumento).
    """

    original_renombre = player.renombre
    player.renombre = min(100, player.renombre + amount)
    player.save()

    # Crear log asociado si se proporciona razón
    if reason and hasattr(player, 'match_set'):
        last_match = player.match_set.order_by('-scheduled_at').first()
        if last_match:
            create_match_log(
                match=last_match,
                event=f"Renombre incrementado en {amount} por: {reason}",
                player=player
            )

    print(f"Renombre aumentado para {player}: {original_renombre} → {player.renombre}")
    return player

def process_final_match(tournament, completed_matches_queryset):
    """
    Procesa la lógica de un torneo cuando se completa la última partida
    y determina al ganador del torneo. También actualiza el estado del torneo
    y distribuye las recompensas entre los jugadores ganadores.
    
    Argumentos:
    tournament (Tournament): El torneo cuyo resultado final se va a procesar.
    completed_matches_queryset (QuerySet): Un conjunto de partidos completados.
    """
    # Obtener la última partida completada (la más reciente)
    last_match = completed_matches_queryset.first()  # 'first()' da el primer partido completado

    if last_match and last_match.winner:  # Verificar si la última partida tiene un ganador
        winner = last_match.winner  # El ganador del torneo es el ganador de la última partida
        print(f"   ✅ El ganador de la última partida es: {winner.name}")

        # Uso de una transacción atómica para garantizar la consistencia de las operaciones
        with transaction.atomic():
            # Actualizar el ganador del torneo y cambiar su estado a 'completed' (finalizado)
            tournament.winner = winner
            tournament.status = 'completed'
            tournament.save()  # Guardar los cambios en el torneo

            # Obtener a todos los jugadores del equipo ganador
            players = winner.player_set.all()

            # Si el torneo tiene un premio en efectivo, distribuirlo entre los jugadores
            if players.exists() and tournament.prize_pool:
                reward_per_player = tournament.prize_pool / players.count()  # Dividir el pool de premios entre los jugadores
                for player in players:
                    # Si el jugador es Premium, recibe el doble de recompensa
                    if player.role == "Premium":
                        player.coins += reward_per_player * 2
                    else:
                        player.coins += reward_per_player  # Jugador regular recibe la recompensa normal
                    player.save()  # Guardar los cambios en el jugador

            # Enviar correos electrónicos a los jugadores del equipo ganador
            for player in players:
                send_mail(
                    subject='✅ ¡Torneo finalizado!',  # Asunto del correo
                    message=(
                        f'Hola {player.user.username},\n\n'  # Saludo al jugador
                        'El torneo ha finalizado correctamente.\n\n'
                        f'Enhorabuena por ganar el torneo!!\n\n'  # Felicitaciones por ganar
                        '- El equipo de ArenaGG'  # Firma
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,  # Remitente configurado en settings
                    recipient_list=[player.user.email],  # Correo del jugador
                    fail_silently=False,  # Si ocurre un error, lanzará una excepción
                )

        # Imprimir un mensaje de confirmación en consola
        print(f"   🏅 Torneo finalizado. Ganador: {winner.name}")
    else:
        # Si no se puede determinar el ganador, mostrar un mensaje de advertencia
        print("   ⚠️ No se pudo determinar el ganador del partido completado.")



def process_round(tournament, completed_matches_queryset, round_number):
    """
    Procesa la lógica para generar los partidos de la siguiente ronda
    del torneo, usando los equipos ganadores de la ronda anterior.

    Argumentos:
    tournament (Tournament): El torneo en el que se generarán los partidos.
    completed_matches_queryset (QuerySet): Un conjunto de partidos completados en la ronda anterior.
    round_number (int): El número de la ronda actual del torneo (por ejemplo, ronda 2, ronda 3, etc.)
    """
    # Crear una lista para almacenar los equipos ganadores
    winning_teams = []

    # Iterar sobre los partidos completados de la ronda anterior
    for match in completed_matches_queryset:
        if match.winner:  # Verificar si el partido tiene un ganador
            winning_teams.append(match.winner)  # Agregar el equipo ganador a la lista

    # Verificar si el número de equipos ganadores coincide con el número esperado para la ronda
    if len(winning_teams) == (round_number * 2):  # Se espera el doble de equipos en cada ronda
        # Generar los partidos para la siguiente ronda usando los equipos ganadores
        generate_matches_by_mmr(tournament.id, round=round_number, tournament_teams=winning_teams)
        print(f"   ✅ Generados partidos para la ronda {round_number}.")  # Confirmación en consola
    else:
        # Si no se pudieron determinar los ganadores de todos los partidos, mostrar un mensaje de advertencia
        print(f"   ⚠️ No se pudo determinar el ganador de todas las partidas completadas para la ronda {round_number}.")
