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
            continue

        if now >= match.scheduled_at and match.status != "completed":
            if match.team1_ready and not match.team2_ready:
                winner = match.team1
                team1_score, team2_score = 1, 0
                reason = "solo el equipo 1 estaba listo"
                for player in match.team2.players.all():
                    decrease_player_renombre(player, 5, "No se ha presentado")
            elif match.team2_ready and not match.team1_ready:
                winner = match.team2
                team1_score, team2_score = 0, 1
                reason = "solo el equipo 2 estaba listo"
                for player in match.team1.players.all():
                    decrease_player_renombre(player, 5, "No se ha presentado")
            else:
                winner = random.choice([match.team1, match.team2])
                team1_score, team2_score = (1, 0) if winner == match.team1 else (0, 1)
                reason = "ningún equipo estaba listo, ganador aleatorio"
                for player in match.team2.player_set.all():
                    decrease_player_renombre(player, 5, "No se ha presentado")

                for player in match.team1.player_set.all():
                    decrease_player_renombre(player, 5, "No se ha presentado")

            record_match_result(match, winner, team1_score, team2_score)
            create_match_log(match, f"Partido finalizado automáticamente. Ganador: {winner.name} ({reason}).")
            print(f"  🏁 Resultado automático registrado. {winner.name} gana {team1_score}-{team2_score}.")
        else:
            print("  ⌛ Aún no es la hora o ya se registró resultado.")

    print("[DEBUG] Tarea 'check_teams_ready_for_match' finalizada.")


