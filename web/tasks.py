from celery import shared_task
from django.utils import timezone
from .models import *
from itertools import zip_longest
from django.core.mail import send_mail
from .functions import generate_matches_by_mmr


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

            # Si el estado cambia a 'ongoing' y no se han generado las partidas, generar las partidas
            if new_status == 'ongoing' and not tournament.matches_generated:
                print(f"  Generando partidas para el torneo {tournament.name}...")
                generate_matches_by_mmr(tournament.id)  # Llamada a la tarea de generar partidas
                print(f"  ✅ Partidas generadas.")


        else:
            print(f"  ⏩ Estado ya era correcto. No se guarda.")




