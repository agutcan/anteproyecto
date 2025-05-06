from functools import total_ordering

from celery import shared_task
from django.utils import timezone
from .models import *
from .functions import *
import random


@shared_task
def update_tournament_status():
    now = timezone.now()
    print(f"[DEBUG] Ejecutando task a las: {now}")

    tournaments = Tournament.objects.filter(status__icontains="upcoming")
    for tournament in tournaments:
        print(f"[DEBUG] Torneo: {tournament.name}")
        print(f"  Start: {tournament.start_date}")
        print(f"  Status actual: {tournament.status}")

        if tournament.start_date <= now and tournament.status != "completed":
            new_status = 'ongoing'
        else:
            new_status = 'upcoming'

        print(f"  Nuevo status: {new_status}")

        if tournament.status != new_status:
            tournament.status = new_status
            tournament.save()
            print(f"  ✅ Estado actualizado a: {new_status}")

            # Si el estado cambia a 'ongoing' y no se han generado las partidas, generar las partidas
            if new_status == 'ongoing' and not tournament.matches_generated:
                print(f"  Generando partidas para el torneo {tournament.name}...")
                generate_matches_by_mmr(tournament.id)  # Llamada a la tarea de generar partidas
                print(f"  ✅ Partidas generadas.")

        else:
            print(f"  ⏩ Estado ya era correcto. No se guarda.")

@shared_task
def check_teams_ready_for_match():
    now = timezone.now()
    print(f"[DEBUG] Ejecutando task a las: {now}")

    matches = Match.objects.filter(status='pending')
    for match in matches:
        print(f"[DEBUG] Partido: {match.team1.name} vs {match.team2.name}")
        print(f"  Fecha y hora programada: {match.scheduled_at}")
        print(f"  Estado actual: {match.status}")

        if match.team1_ready and match.team2_ready:
            match.status = "ongoing"
            match.save()
            create_match_log(match, "Ambos equipos listos. El partido ha comenzado.")
            print("  ✅ Partido marcado como 'ongoing'.")
            for player in match.team1.player_set.all():
                # Enviar correo de confirmación
                send_mail(
                    subject='✅ ¡Partida Comenzada!',
                    message=(
                        f'Hola {player.user},\n\n'
                        'La partida ha comenzado correctamente.\n\n'
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
                        'La partida ha comenzado correctamente.\n\n'
                        '- El equipo de ArenaGG'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[player.user.email],
                    fail_silently=False,
                )
            continue

        if now >= match.scheduled_at and match.status != "completed":
            if match.team1_ready and not match.team2_ready:
                winner = match.team1
                team1_score, team2_score = 1, 0
                match.winner = winner
                match.save()
                reason = "solo el equipo 1 estaba listo"
                update_players_stats(match.team1, True)
                update_players_stats(match.team2)
                for player in match.team2.player_set.all():
                    decrease_player_renombre(player, 5, "No se ha presentado")

            elif match.team2_ready and not match.team1_ready:
                winner = match.team2
                team1_score, team2_score = 0, 1
                match.winner = winner
                match.save()
                reason = "solo el equipo 2 estaba listo"
                update_players_stats(match.team1)
                update_players_stats(match.team2, True)

                for player in match.team1.players.all():
                    decrease_player_renombre(player, 5, "No se ha presentado")

            else:
                winner = random.choice([match.team1, match.team2])
                team1_score, team2_score = (1, 0) if winner == match.team1 else (0, 1)
                match.winner = winner
                match.save()
                reason = "ningún equipo estaba listo, ganador aleatorio"
                for player in match.team2.player_set.all():
                    decrease_player_renombre(player, 5, "No se ha presentado")

                for player in match.team1.player_set.all():
                    decrease_player_renombre(player, 5, "No se ha presentado")

                if winner == match.team1:
                    update_players_stats(match.team1, True)
                    update_players_stats(match.team2)
                else:
                    update_players_stats(match.team2, True)
                    update_players_stats(match.team1)


            record_match_result(match, winner, team1_score, team2_score)
            create_match_log(match, f"Partido finalizado automáticamente. Ganador: {winner.name} ({reason}).")
            print(f"  🏁 Resultado automático registrado. {winner.name} gana {team1_score}-{team2_score}.")
        else:
            print("  ⌛ Aún no es la hora o ya se registró resultado.")

    print("[DEBUG] Tarea 'check_teams_ready_for_match' finalizada.")


@shared_task
def check_tournament_match_progress():
    now = timezone.now()
    print(f"[DEBUG] Ejecutando tarea de verificación de torneos a las: {now}")

    ongoing_tournaments = Tournament.objects.filter(status='ongoing')
    if not ongoing_tournaments.exists():
        print("[INFO] No hay torneos en curso.")
        return

    for tournament in ongoing_tournaments:
        ongoing_matches = Match.objects.filter(tournament=tournament, status='ongoing').count()
        completed_matches = Match.objects.filter(tournament=tournament, status='completed').count()
        total_matches = Match.objects.filter(tournament=tournament).count()
        team_count = tournament.tournamentteam_set.count()

        print(f"🏆 Torneo: {tournament.name}")
        print(f"   🔄 Partidas en curso: {ongoing_matches}")
        print(f"   ✅ Partidas completadas: {completed_matches}")
        print(f"   📊 Total de partidas: {total_matches}")
        print(f"   📊 Total de equipos: {team_count}")

        # Obtener las partidas completadas
        completed_matches_queryset = Match.objects.filter(tournament=tournament, status='completed')

        if team_count == 2 and completed_matches == 1:
            process_final_match(tournament, completed_matches_queryset)

        elif team_count == 4:
            if completed_matches == 2:
                process_round(tournament, completed_matches_queryset, round_number=2)
            elif completed_matches == 4:
                process_final_match(tournament, completed_matches_queryset)

        elif team_count == 8:
            if completed_matches == 4:
                process_round(tournament, completed_matches_queryset, round_number=2)
            elif completed_matches == 6:
                process_round(tournament, completed_matches_queryset, round_number=3)
            elif completed_matches == 8:
                process_final_match(tournament, completed_matches_queryset)

    print("[DEBUG] Tarea 'check_tournament_match_progress' finalizada.")
