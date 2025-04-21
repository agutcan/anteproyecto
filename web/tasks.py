from celery import shared_task
from django.utils import timezone
from .models import *
from itertools import zip_longest
from django.core.mail import send_mail


@shared_task
def update_tournament_status():
    now = timezone.now()
    print(f"[DEBUG] Ejecutando task a las: {now}")

    tournaments = Tournament.objects.all()
    for tournament in tournaments:
        print(f"[DEBUG] Torneo: {tournament.name}")
        print(f"  Start: {tournament.start_date}")
        print(f"  End:   {tournament.end_date}")
        print(f"  Status actual: {tournament.status}")

        if tournament.start_date <= now < tournament.end_date:
            new_status = 'ongoing'
        elif now >= tournament.end_date:
            new_status = 'completed'
        else:
            new_status = 'upcoming'

        print(f"  Nuevo status: {new_status}")

        if tournament.status != new_status:
            tournament.status = new_status
            tournament.save()
            print(f"  ✅ Estado actualizado a: {new_status}")
        else:
            print(f"  ⏩ Estado ya era correcto. No se guarda.")


@shared_task
def generate_matches_by_mmr(tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)

    # Verificar el número de equipos en el torneo
    tournament_teams = TournamentTeam.objects.filter(tournament=tournament).select_related('team')
    num_teams = tournament_teams.count()

    # Si el número de equipos es impar, eliminamos el torneo y notificamos a los jugadores
    if num_teams % 2 != 0:
        # Enviar correo a todos los jugadores del torneo
        players = Player.objects.filter(team__tournamentteam__tournament=tournament)
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
                team1=team1.team,
                team2=team2.team,
                scheduled_date=timezone.now()  # O puedes asignar una fecha específica
            )

    # Marcar que los partidos han sido generados
    tournament.matches_generated = True
    tournament.save()