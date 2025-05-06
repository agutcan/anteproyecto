from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from .models import *
from django.db import transaction
from itertools import zip_longest

def update_players_stats(team, is_winner=False):
    """Actualiza las estadísticas, renombre y MMR de los jugadores de un equipo."""
    for player in team.player_set.all():
        player.games_played += 1
        if is_winner:
            player.games_won += 1

        # Actualizar winrate
        player.update_winrate()

        # Actualizar MMR
        if is_winner:
            player.mmr += 10
        else:
            player.mmr = max(10, player.mmr - 5)

        # Aumentar renombre si gana
        if is_winner:
            increase_player_renombre(player, amount=5, reason="Victoria en partido oficial")

        player.save()


def generate_matches_by_mmr(tournament_id, round=1, tournament_teams=None):
    tournament = Tournament.objects.get(id=tournament_id)

    # Verificar el número de equipos en el torneo
    if not tournament_teams:
        tournament_teams = TournamentTeam.objects.filter(tournament=tournament).select_related('team')
    num_teams = tournament_teams.count()

    # Si el número de equipos es impar o 0, eliminamos el torneo y notificamos a los jugadores
    if num_teams == 0 or num_teams % 2 != 0:
        # Enviar correo a todos los jugadores del torneo
        players = Player.objects.filter(team__tournamentteam__tournament=tournament).select_related('tournament')
        for player in players:
            send_mail(
                'Torneo Cancelado',
                f'Hola {player.user.username},\n\nLamentablemente, el torneo {tournament.name} ha sido cancelado debido a un número impar de equipos.',
                'administracion@arenagg.com',  # Asegúrate de tener configurado un remitente válido
                [player.user.email],
                fail_silently=False,
            )

        # Eliminar el torneo
        tournament.delete()
        print(f"⚠️ El torneo {tournament.name} ha sido cancelado debido a un número impar de equipos.")
        return

    # Procedemos a generar los partidos si el número de equipos es par
    team_mmr_pairs = []
    for tt in tournament_teams:
        avg_mmr = tt.team.get_avg_mmr()  # Obtener el MMR promedio del equipo
        team_mmr_pairs.append((tt, avg_mmr))

    # Ordenar los equipos por su MMR
    team_mmr_pairs.sort(key=lambda x: x[1])

    # Emparejar equipos por MMR
    pairings = list(zip_longest(team_mmr_pairs[::2], team_mmr_pairs[1::2]))

    for pair in pairings:
        if pair[0] and pair[1]:
            team1 = pair[0][0]
            team2 = pair[1][0]
            Match.objects.create(
                tournament=tournament,
                round=round,
                scheduled_at=timezone.now() + timezone.timedelta(minutes=5),
                team1=team1.team,
                team2=team2.team,
            )

    # Marcar que los partidos han sido generados
    tournament.matches_generated = True
    tournament.save()

def record_match_result(match, winner, team1_score, team2_score):
    result = MatchResult.objects.create(
        match=match,
        winner=winner,
        team1_score=team1_score,
        team2_score=team2_score
    )

    # Actualizar el estado del partido a 'completed'
    match.status = 'completed'
    match.save()
    for player in match.team1.player_set.all():
        # Enviar correo de confirmación
        send_mail(
            subject='✅ ¡Partida finalizada!',
            message=(
                f'Hola {player.user},\n\n'
                'La partida ha finalizado correctamente.\n\n'
                f'Resultado del partido {match}: {team1_score}-{team2_score}\n\n'
                '- El equipo de ArenaGG'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[player.user.email],
            fail_silently=False,
        )

    for player in match.team2.player_set.all():
        # Enviar correo de confirmación
        send_mail(
            subject='✅ ¡Partida finalizada!',
            message=(
                f'Hola {player.user},\n\n'
                'La partida ha finalizado correctamente.\n\n'
                f'Resultado del partido {match}: {team1_score}-{team2_score}\n\n'
                '- El equipo de ArenaGG'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[player.user.email],
            fail_silently=False,
        )



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
    """Procesa la lógica para un torneo con la última partida completada y determinar al ganador"""
    last_match = completed_matches_queryset.first()
    if last_match and last_match.winner:
        winner = last_match.winner
        print(f"   ✅ El ganador de la última partida es: {winner.name}")
        with transaction.atomic():
            tournament.winner = winner
            tournament.status = 'completed'
            tournament.save()

            players = winner.player_set.all()
            if players.exists() and tournament.prize_pool:
                reward_per_player = tournament.prize_pool / players.count()
                for player in players:
                    if player.role == "Premium":
                        player.coins += reward_per_player * 2
                    else:
                        player.coins += reward_per_player
                    player.save()

            for player in players:
                send_mail(
                    subject='✅ ¡Torneo finalizado!',
                    message=(
                        f'Hola {player.user},\n\n'
                        'El torneo ha finalizado correctamente.\n\n'
                        f'Enhorabuena por ganar el torneo!!\n\n'
                        '- El equipo de ArenaGG'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[player.user.email],
                    fail_silently=False,
                )
            print(f"   🏅 Torneo finalizado. Ganador: {winner.name}")
    else:
        print("   ⚠️ No se pudo determinar el ganador del partido completado.")


def process_round(tournament, completed_matches_queryset, round_number):
    """Genera los partidos para la siguiente ronda"""
    winning_teams = []
    for match in completed_matches_queryset:
        if match.winner:
            winning_teams.append(match.winner)

    if len(winning_teams) == (round_number * 2):  # Se espera el doble de equipos según la ronda
        generate_matches_by_mmr(tournament.id, round=round_number, tournament_teams=winning_teams)
        print(f"   ✅ Generados partidos para la ronda {round_number}.")
    else:
        print(f"   ⚠️ No se pudo determinar el ganador de todas las partidas completadas para la ronda {round_number}.")