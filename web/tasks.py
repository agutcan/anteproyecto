from celery import shared_task
from django.utils import timezone
from .models import Tournament


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
