from django.core.mail import send_mail
from django.utils import timezone
from .models import *
from itertools import zip_longest

def generate_matches_by_mmr(tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)

    # Verificar el número de equipos en el torneo
    tournament_teams = TournamentTeam.objects.filter(tournament=tournament).select_related('team')
    num_teams = tournament_teams.count()

    # Si el número de equipos es impar o 0, eliminamos el torneo y notificamos a los jugadores
    if num_teams == 0 or num_teams % 2 != 0:
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
                round=1,
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

    print(f"Resultado registrado para el partido {match}: {team1_score}-{team2_score}")