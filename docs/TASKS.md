# Explicación de tareas programadas en Django (`tasks.py`)

Este archivo define las tareas programadas utilizadas en la aplicación web. Las tareas programadas representan tareas que se ejecutan constantemente con celery y redis. A continuación, se describen cada una de las tareas:

---

## Tarea: `update_tournament_status`

Esta tarea se ejecuta periódicamente para **actualizar el estado de los torneos** según la fecha de inicio. A continuación, se explica el funcionamiento y los detalles de la tarea.

### Descripción

La tarea `update_tournament_status` realiza las siguientes acciones:

1. **Busca torneos en estado 'upcoming' (próximos)**:  
   La tarea filtra los torneos cuyo estado es **'upcoming'**, es decir, aquellos que están programados para empezar en el futuro.

2. **Actualiza el estado de los torneos**:  
   - Si la fecha de inicio de un torneo ha pasado y su estado actual no es 'completed', el estado del torneo se cambia a **'ongoing'** (en curso).
   - Si el estado del torneo cambia a 'ongoing' y aún no se han generado las partidas, la tarea invoca la función `generate_matches_by_mmr` para generarlas.

3. **Optimización en la actualización del estado**:  
   La tarea solo actualiza el estado del torneo si ha cambiado, lo que ayuda a **evitar escrituras innecesarias en la base de datos**.

```python
@shared_task
def update_tournament_status():
    """
    Tarea periódica para actualizar el estado de los torneos según la fecha de inicio.

    Esta tarea realiza las siguientes acciones:
    - Busca todos los torneos con estado 'upcoming' (próximos).
    - Si la fecha de inicio del torneo ha pasado y su estado no es 'completed', se cambia su estado a 'ongoing'.
    - Si el estado del torneo cambia a 'ongoing' y aún no se han generado las partidas, se invoca la función
      `generate_matches_by_mmr` para generarlas.
    - Guarda el nuevo estado solo si ha cambiado, para evitar escrituras innecesarias en la base de datos.

    Salida por consola (para depuración):
    - Imprime la hora de ejecución de la tarea.
    - Detalla el estado actual y el nuevo estado de cada torneo procesado.
    - Indica si se han generado partidas nuevas.

    Esta tarea está pensada para ejecutarse de forma periódica mediante Celery Beat.
    """
    now = timezone.now()  # Obtiene la hora y fecha actual del servidor (con zona horaria).

    # Filtra los torneos cuyo estado actual contiene la palabra 'upcoming' (es decir, que aún no han comenzado).
    tournaments = Tournament.objects.filter(status__icontains="upcoming")
    
    # Itera sobre cada torneo encontrado
    for tournament in tournaments:

        # Determina si el torneo debe cambiar a 'ongoing' según la fecha actual y su estado actual
        if tournament.start_date <= now and tournament.status != "completed":
            new_status = 'ongoing'
        else:
            new_status = 'upcoming'
        

        # Solo actualiza si el estado ha cambiado
        if tournament.status != new_status:
            tournament.status = new_status  # Actualiza el campo status
            tournament.save()  # Guarda los cambios en la base de datos

            # Si el torneo pasa a estado 'ongoing' y aún no se han generado las partidas
            if new_status == 'ongoing' and not tournament.matches_generated:
                generate_matches_by_mmr(tournament.id)  # Llama a la función que genera las partidas
```

## Tarea: `check_teams_ready_for_match`

Esta tarea se ejecuta periódicamente para **verificar el estado de los partidos pendientes** y actuar en consecuencia. A continuación se explica su funcionamiento y detalle.

### Descripción

La tarea `check_teams_ready_for_match` realiza las siguientes acciones:

1. **Verificación de la preparación de los equipos**:  
   La tarea verifica si ambos equipos están listos antes de la hora programada del partido:
   - Si ambos equipos están listos, se marca el partido como **'ongoing'** y se notifica a los jugadores por correo electrónico.
   - Si no se alcanzó la hora programada y uno o ambos equipos no están listos:
     - Se declara el ganador al equipo que esté presente.
     - Si ninguno está listo, se elige un ganador aleatorio.
   - Las estadísticas de los jugadores y equipos se actualizan según el resultado.
   - Se penaliza a los jugadores ausentes con pérdida de renombre.
   
2. **Registro automático de resultados**:  
   Después de determinar el ganador, se guarda el resultado automáticamente mediante la función `record_match_result` y se genera un log del partido.

3. **Optimización**:  
   Solo se procesan partidos cuyo estado es **'pending'** y la tarea solo realiza acciones si es necesario, evitando ejecuciones innecesarias.

### Código:

```python
@shared_task
def check_teams_ready_for_match():
    """
    Tarea periódica para verificar el estado de los partidos pendientes y actuar en consecuencia.

    Funcionalidades principales:
    - Si ambos equipos están listos antes de la hora programada, se marca el partido como 'ongoing'
      y se notifica a los jugadores por correo electrónico.
    - Si se alcanza la hora programada y uno o ambos equipos no están listos:
        - Se declara ganador al equipo que esté presente.
        - Si ninguno está listo, se elige un ganador al azar.
        - Se actualizan estadísticas y se penaliza con pérdida de renombre a jugadores ausentes.
    - En todos los casos, se registra el resultado automáticamente mediante `record_match_result`
      y se guarda un log del partido.

    Esta tarea debe ejecutarse de forma periódica mediante Celery Beat o similar.
    """
    # Obtiene la fecha y hora actual con zona horaria
    now = timezone.now()

    # Filtra todos los partidos pendientes en la base de datos
    matches = Match.objects.filter(status='pending')

    # Procesa uno por uno
    for match in matches:

        # Caso 1: Ambos equipos están listos antes de la hora de inicio
        if match.team1_ready and match.team2_ready:
            # Se inicia el partido
            match.status = "ongoing"
            match.save()
            create_match_log(match, "Ambos equipos listos. El partido ha comenzado.")

            # Notifica a cada jugador del equipo 1 por correo electrónico
            for player in match.team1.player_set.all():
                send_mail(
                    subject='✅ ¡Partida Comenzada!',
                    message=(f'Hola {player.user},\n\nLa partida ha comenzado correctamente.\n\n- El equipo de ArenaGG'),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[player.user.email],
                    fail_silently=False,
                )

            # Notifica a cada jugador del equipo 2 por correo electrónico
            for player in match.team2.player_set.all():
                send_mail(
                    subject='✅ ¡Partida finalizada!',
                    message=(f'Hola {player.user},\n\nLa partida ha comenzado correctamente.\n\n- El equipo de ArenaGG'),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[player.user.email],
                    fail_silently=False,
                )

            # Pasa al siguiente partido (no continúa evaluando condiciones)
            continue

        # Caso 2: Ya es hora del partido y aún no se ha completado
        if now >= match.scheduled_at and match.status != "completed":

            # Subcaso: solo el equipo 1 está listo
            if match.team1_ready and not match.team2_ready:
                winner = match.team1
                team1_score, team2_score = 1, 0
                match.winner = winner
                match.save()
                reason = "solo el equipo 1 estaba listo"

                # Actualiza estadísticas: equipo 1 gana, equipo 2 pierde
                update_players_stats(match.team1, True)
                update_players_stats(match.team2)

                # Penaliza a los jugadores del equipo 2 por inasistencia
                for player in match.team2.player_set.all():
                    decrease_player_renombre(player, 5, "No se ha presentado")

            # Subcaso: solo el equipo 2 está listo
            elif match.team2_ready and not match.team1_ready:
                winner = match.team2
                team1_score, team2_score = 0, 1
                match.winner = winner
                match.save()
                reason = "solo el equipo 2 estaba listo"

                update_players_stats(match.team1)
                update_players_stats(match.team2, True)
                
                # Penaliza a los jugadores del equipo 1 por inasistencia
                for player in match.team1.player_set.all():  
                    decrease_player_renombre(player, 5, "No se ha presentado")

            # Subcaso: ningún equipo está listo → se elige un ganador aleatoriamente
            else:
                winner = random.choice([match.team1, match.team2])
                team1_score, team2_score = (1, 0) if winner == match.team1 else (0, 1)
                match.winner = winner
                match.save()
                reason = "ningún equipo estaba listo, ganador aleatorio"

                # Penaliza a jugadores de ambos equipos
                for player in match.team2.player_set.all():
                    decrease_player_renombre(player, 5, "No se ha presentado")
                for player in match.team1.player_set.all():
                    decrease_player_renombre(player, 5, "No se ha presentado")

                # Registra la victoria del equipo seleccionado aleatoriamente
                if winner == match.team1:
                    update_players_stats(match.team1, True)
                    update_players_stats(match.team2)
                else:
                    update_players_stats(match.team2, True)
                    update_players_stats(match.team1)

            # Guarda resultado y genera un log del partido
            record_match_result(match, winner, team1_score, team2_score)
            create_match_log(
                match,
                f"Partido finalizado automáticamente. Ganador: {winner.name} ({reason})."
            )

```

## Tarea: `check_tournament_match_progress`

Esta tarea se ejecuta periódicamente para **revisar el progreso de los torneos en curso**. A continuación, se detallan las funciones y el flujo de la tarea.

### Descripción

La tarea `check_tournament_match_progress` realiza las siguientes acciones:

1. **Verificación de los torneos en curso**:  
   La tarea filtra los torneos cuyo estado es **'ongoing'** (en curso).

2. **Cálculo del progreso del torneo**:  
   Para cada torneo en curso:
   - Se cuenta el número de partidos **en curso** y **completados**.
   - Se obtiene el **número total de partidos** y el **número de equipos**.

3. **Determinación de la siguiente fase**:  
   Según el número de equipos y el progreso de los partidos, la tarea decide:
   - Si debe procesarse una **ronda intermedia** (semifinales, cuartos de final, etc.).
   - Si debe procesarse la **final** y finalizar el torneo.

4. **Flujo de procesamiento según el número de equipos**:  
   - Para **torneos de 2 equipos**, después de 1 partido completado, se procesa la final.
   - Para **torneos de 4 equipos**, después de 2 partidos completados, se procesa la segunda ronda (semifinales), y si se han jugado 3 partidos, se procesa la final.
   - Para **torneos de 8 equipos**, después de 4 partidos completados, se procesan las semifinales, y tras 6 partidos completados, se procesa la final.

5. **Optimización**:  
   Solo se procesan los torneos cuyo estado es **'ongoing'** y la tarea realiza acciones solo si es necesario, evitando ejecuciones innecesarias.

### Código:

```python
@shared_task
def check_tournament_match_progress():
    """
    Tarea periódica que revisa el progreso de los torneos en curso.

    Funciones principales:
    - Comprobar cuántos partidos se han jugado en cada torneo 'ongoing'.
    - Según el número de equipos y partidos completados, determina si:
        - Debe procesarse una ronda intermedia (semifinales, cuartos, etc.).
        - Debe procesarse la final y finalizar el torneo.
    """

    # Obtener la hora actual con zona horaria
    now = timezone.now()

    # Buscar torneos que estén en curso
    ongoing_tournaments = Tournament.objects.filter(status='ongoing')
    if not ongoing_tournaments.exists():
        return

    # Procesar cada torneo en curso
    for tournament in ongoing_tournaments:
        # Obtener métricas del torneo
        ongoing_matches = Match.objects.filter(tournament=tournament, status='ongoing').count()
        completed_matches = Match.objects.filter(tournament=tournament, status='completed').count()
        total_matches = Match.objects.filter(tournament=tournament).count()
        team_count = tournament.tournamentteam_set.count()

        # Obtener queryset reutilizable de partidas finalizadas
        completed_matches_queryset = Match.objects.filter(tournament=tournament, status='completed')

        # Lógica para torneos de 2 equipos (1 final directa)
        if team_count == 2 and completed_matches == 1:
            process_final_match(tournament, completed_matches_queryset)

        # Torneos de 4 equipos:
        # - 2 partidos completados → procesar ronda 2 (final)
        # - 3 partidos completados → ya se jugó la final → finalizar
        elif team_count == 4:
            if completed_matches == 2:
                process_round(tournament, completed_matches_queryset, round_number=2)
            elif completed_matches == 3:
                process_final_match(tournament, completed_matches_queryset)

        # Torneos de 8 equipos:
        # - 4 partidos completados → procesar ronda 2 (semifinales)
        # - 6 partidos completados → procesar ronda 3 (final)
        # - 7 partidos completados → finalizar torneo
        elif team_count == 8:
            if completed_matches == 4:
                process_round(tournament, completed_matches_queryset, round_number=2)
            elif completed_matches == 6:
                process_round(tournament, completed_matches_queryset, round_number=3)
            elif completed_matches == 7:
                process_final_match(tournament, completed_matches_queryset)

```

## 🔄 Navegación
[⬅️ Volver al README principal](../README.md)
