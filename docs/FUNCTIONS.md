# 📄 Explicación de Funciones en Django (`functions.py`)

Este archivo define las funciones utilizadas en la aplicación web. Las funciones representan bloques de código reutilizables que realizan una tarea específica. A continuación, se describen cada una de las funciones:

---

## 📊 Función `update_winrate`

### 📌 Descripción  
Actualiza el porcentaje de victorias (`winrate`) de un jugador, basado en la relación entre partidas ganadas y jugadas.

### 📋 Parámetros  
| Parámetro  | Tipo   | Descripción                                           | Opcional |
|------------|--------|-------------------------------------------------------|----------|
| `player`   | Player | Instancia del jugador cuyos datos serán actualizados | ❌ No    |

### 🔄 Comportamiento  
1. Si el jugador ha disputado al menos una partida (`games_played > 0`):  
   - Calcula el `winrate` como:  
     \(`games_won` / `games_played`) × 100  
2. Si no ha jugado partidas, establece el `winrate` en **0.0**.  
3. Guarda el objeto `player` con los cambios aplicados (`player.save()`).

```python
def update_winrate(player):
    """
    Actualiza el porcentaje de victorias (winrate) de un jugador basado en sus estadísticas.
    
    Calcula el winrate como (games_won / games_played) * 100 y guarda el resultado.
    Si no hay partidas jugadas, establece el winrate a 0.0.

    Args:
        player: Instancia del modelo Player que debe contener:
            - games_played (int): Número total de partidas jugadas
            - games_won (int): Número de partidas ganadas
            - winrate (float): Atributo que será actualizado
            - save(): Método para guardar los cambios en la base de datos

    Returns:
        None: La función no retorna nada, pero modifica y guarda el objeto player
    """
    
    if player.games_played > 0:
        player.winrate = (player.games_won / player.games_played) * 100
    else:
        player.winrate = 0.0
    player.save()
```

---

## 🏅 Función `update_players_stats`

### 📌 Descripción  
Actualiza las estadísticas de los jugadores de un equipo después de un partido, modificando:  
- Partidos jugados (`games_played`)  
- Partidos ganados (`games_won`)  
- Winrate (`winrate`)  
- Puntuación MMR (`mmr`)  
- Renombre (`renombre`)  

### 📋 Parámetros  
| Parámetro   | Tipo  | Descripción                              | Opcional |  
|-------------|-------|------------------------------------------|----------|  
| `team`      | Team  | Equipo cuyos jugadores se actualizarán   | ❌ No    |  
| `is_winner` | bool  | Si el equipo ganó el partido (default: `False`) | ✔️ Sí    |  


### 🔄 Comportamiento  
1. **Para cada jugador del equipo**:  
   - Incrementa `games_played` en 1.  
   - Si `is_winner=True`:  
     - Incrementa `games_won` en 1.  
     - Aumenta `mmr` en **+10**.  
     - Aumenta `renombre` en **+5** (usando `increase_player_renombre`).  
   - Si `is_winner=False`:  
     - Reduce `mmr` en **-5** (pero nunca por debajo de 10).  
   - Actualiza automáticamente el `winrate` (llamando a `player.update_winrate()`).  
   - Guarda los cambios en la base de datos (`player.save()`).  

### ⚠️ Restricciones  
- El `mmr` **nunca** puede ser menor que 10.  
- El `renombre` solo se modifica en caso de victoria.

```python
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

```

## 🏅 Función `generate_matches_by_mmr`

### 📌 Descripción  
Genera los partidos de un torneo basándose en el MMR promedio de los equipos participantes.  
- Empareja equipos con MMR similares (el más bajo contra el segundo más bajo, etc.).  
- Cancela el torneo si no hay equipos suficientes (2, 4 u 8).  
- Programa los partidos automáticamente.  

### 📋 Parámetros  
| Parámetro          | Tipo        | Descripción                                  | Opcional |  
|--------------------|-------------|----------------------------------------------|----------|  
| `tournament_id`    | int         | ID del torneo en la base de datos.          | ❌ No    |  
| `round`            | int         | Número de ronda actual (default: `1`).      | ✔️ Sí    |  
| `tournament_teams` | QuerySet    | Lista de equipos del torneo (si no se pasa, se consulta la BD). | ✔️ Sí    |  


### 🔄 Comportamiento  

1. **Validación de equipos**  
   - Si no hay equipos (`num_teams == 0`) o el número no es 2, 4 u 8:  
     - Envía un correo a todos los jugadores notificando la cancelación.  
     - Elimina el torneo de la base de datos.  
     - **Ejemplo de correo**:  
       ```plaintext
       Asunto: Torneo Cancelado  
       Mensaje: "Hola {username}, el torneo {torneo} ha sido cancelado por número impar de equipos."  
       ```
   - Si no hay suficientes jugadores en un equipo:
      - Envía un correo a todos los jugadores notificando la cancelación.
      - Elimina el torneo de la base de datos.  

2. **Generación de partidos**  
   - Calcula el MMR promedio de cada equipo (usando `team.get_avg_mmr()`).  
   - Ordena equipos de **menor a mayor MMR**.  
   - Empareja:  
     - **1° vs 2°**, **3° vs 4°**, etc. (usando `zip_longest` para evitar desbordamiento).  
   - Crea partidos en la BD con:  
     - **Hora de inicio**: 2 minutos después de la generación (`timezone.now() + timedelta(minutes=2)`).  

3. **Actualización del torneo**  
   - Marca `matches_generated = True` en el torneo.  


## ⚠️ Restricciones  
- **Solo funciona** con 2, 4 u 8 equipos y con equipos completos (otros valores cancelan el torneo).  
- **Requiere**:  
  - Método `get_avg_mmr()` en el modelo `Team`.  
  - Configuración correcta de `send_mail` (servidor SMTP).  

```python
def generate_matches_by_mmr(tournament_id, round=1, tournament_teams=None):
    """
    Genera los partidos de un torneo basándose en el MMR promedio de los equipos participantes.
    
    Esta función realiza las siguientes operaciones:
    1. Verifica que el número de equipos sea válido (2, 4 u 8)
    2. Valida que todos los equipos tengan el número correcto de jugadores
    3. Cancela el torneo con notificaciones si no se cumplen las condiciones
    4. Ordena los equipos por MMR promedio y los empareja
    5. Crea los partidos correspondientes en la base de datos

    Args:
        tournament_id (int): ID del torneo en la base de datos. Debe existir un objeto Tournament con este ID.
        round (int, optional): Número de ronda del torneo. Por defecto es 1.
        tournament_teams (QuerySet, optional): Conjunto de equipos del torneo. Si es None, se obtienen de la base de datos.

    Returns:
        None: La función no retorna nada pero puede:
              - Crear partidos en la base de datos
              - Cancelar el torneo (eliminándolo) si hay condiciones inválidas

    Raises:
        Tournament.DoesNotExist: Si no existe un torneo con el ID proporcionado
    """
    
    # Obtener el torneo utilizando el ID proporcionado
    tournament = Tournament.objects.get(id=tournament_id)

    # Verificar el número de equipos en el torneo
    if not tournament_teams:
        # Si no se pasan equipos, los obtenemos desde la base de datos
        tournament_teams = TournamentTeam.objects.filter(tournament=tournament).select_related('team')
    
    # Número total de equipos en el torneo
    num_teams = tournament_teams.count()
    # Si el número de equipos es 0 cancelamos el torneo
    if num_teams == 0 
        # Eliminar el torneo cancelado
        tournament.delete()
        return

    # Si el número es diferente a 2, 4 u 8, cancelamos el torneo
    if num_teams != 2 and num_teams != 4 and num_teams != 8:
        # Enviar correo a todos los jugadores del torneo notificando la cancelación
        players = Player.objects.filter(team__tournamentteam__tournament=tournament).select_related('team')
        for player in players:
            send_mail(
                subject='Torneo Cancelado',  # Asunto del correo
                message=f'Hola {player.user.username},\n\nLamentablemente, el torneo {tournament.name} ha sido cancelado debido a un número impar de equipos.',
                from_email=settings.DEFAULT_FROM_EMAIL,  # Remitente (asegúrate de configurar un remitente válido)
                recipient_list=[player.user.email],  # Correo del jugador
                fail_silently=False,  # Si ocurre un error, lanzar una excepción
            )

        # Eliminar el torneo cancelado
        tournament.delete()
        return

    # Verificar que todos los equipos tengan la cantidad exacta de jugadores
    invalid_teams = []
    for team in Team.objects.filter(tournamentteam__tournament=tournament):
        if team.player_set.count() != tournament.max_player_per_team:
            invalid_teams.append(team)

    if invalid_teams:
        players = Player.objects.filter(team__in=invalid_teams)
        for player in players:
            send_mail(
                subject='Torneo Cancelado',
                message=f'Hola {player.user.username},\n\nLamentablemente, el torneo {tournament.name} ha sido cancelado porque algunos equipos no tienen el número correcto de jugadores.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[player.user.email],
                fail_silently=False,
            )

        tournament.delete()
        return

    # Si el número de equipos es par, procedemos a generar los partidos
    team_mmr_pairs = []
    for tt in tournament_teams:
        # Obtener el MMR promedio del equipo
        avg_mmr = tt.team.get_avg_mmr() 
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
                scheduled_at=timezone.now() + timezone.timedelta(minutes=2),  # Programar el partido para dentro de 2 minutos
                team1=team1.team,  # Asignar el primer equipo
                team2=team2.team,  # Asignar el segundo equipo
            )

    # Marcar que los partidos han sido generados y guardar el estado del torneo
    tournament.matches_generated = True
    tournament.save()

```

---

## 🏅 Función `record_match_result`

### 📌 Descripción  
Registra el resultado de un partido en la base de datos, actualiza su estado a "completado" y notifica vía email a todos los jugadores involucrados.  

### 📋 Parámetros  
| Parámetro       | Tipo  | Descripción                                  |  
|-----------------|-------|----------------------------------------------|  
| `match`        | Match | Objeto del partido a registrar.             |  
| `winner`       | Team  | Equipo ganador del partido.                 |  
| `team1_score`  | int   | Puntuación del equipo 1.                    |  
| `team2_score`  | int   | Puntuación del equipo 2.                    |  

### 🔄 Flujo de Ejecución  

1. **Registro del Resultado**  
   - Crea un registro en `MatchResult` con:  
     ```python
     MatchResult.objects.create(
         match=match,
         winner=winner,
         team1_score=team1_score,
         team2_score=team2_score
     )
     ```  

2. **Actualización del Partido**  
   - Cambia el estado del partido a `completed`:  
     ```python
     match.status = 'completed'
     match.save()
     ```  

3. **Notificaciones por Email**  
   - **Envía a todos los jugadores de ambos equipos** un email con:  
     - **Asunto**: `✅ ¡Partida finalizada!`  
     - **Cuerpo**:  
       ```plaintext
       Hola {username},
       La partida ha finalizado correctamente.
       Resultado del partido {match}: {team1_score}-{team2_score}
       - El equipo de ArenaGG
       ```  
   - **Configuración**:  
     - Remitente: `settings.DEFAULT_FROM_EMAIL` (configurado en Django).  
     - Error handling: `fail_silently=False` (lanza excepciones si falla).  

```python
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

---

## 🔔 Función `create_notification`

Esta función centraliza la creación de notificaciones internas de la plataforma.

### Comportamiento
- Recibe un `user` principal obligatorio.
- Puede añadir destinatarios adicionales con `recipient_users`.
- Crea una única fila en `Notification`.
- Asocia los destinatarios al campo ManyToMany.
- Devuelve la notificación creada para poder encadenar lógica adicional.

### Uso típico
- Torneos creados
- Expulsión de jugadores
- Mensajes de soporte
- Avisos administrativos
- Alertas de resultados inconsistentes

```

---

## 🏅 Función `create_match_log`

### 📌 Descripción  
Crea un registro de eventos (log) asociado a un partido, opcionalmente vinculado a un equipo o jugador específico. Retorna el registro creado.

### 📋 Parámetros  

| Parámetro | Tipo | Descripción | Opcional |
|-----------|------|-------------|----------|
| `match` | `Match` | Instancia del partido asociado | ❌ No |
| `event` | `str` | Descripción textual del evento | ❌ No |
| `team` | `Team` | Equipo relacionado al evento | ✔️ Sí |
| `player` | `Player` | Jugador relacionado al evento | ✔️ Sí |

### 🔄 Comportamiento  

1. **Crea registro en BD**  
   - Inserta un nuevo registro en la tabla `MatchLog` con:
     ```python
     MatchLog.objects.create(
         match=match,
         event=event,
         team=team,
         player=player
     )
     ```

2. **Retorno**  
   - Devuelve la instancia del `MatchLog` creado

## ⚠️ Consideraciones  

- **Relaciones opcionales**: Tanto `team` como `player` pueden ser `None`
- **Uso típico**:  
  - Para eventos globales (ej: inicio de partido) → solo `match` y `event`  
  - Para acciones de equipo (ej: timeout) → agregar `team`  
  - Para acciones individuales (ej: gol) → agregar `player`

```python
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
    return log
```
---

## 🏅 Función `decrease_player_renombre`

### 📌 Descripción  
Reduce el renombre de un jugador con un límite mínimo de 1, registra el evento en un log si existe una razón válida y devuelve el jugador actualizado.

### 📋 Parámetros  

| Parámetro | Tipo | Descripción | Opcional | Restricciones |
|-----------|------|-------------|----------|---------------|
| `player` | `Player` | Jugador afectado | ❌ No | - |
| `amount` | `int` | Cantidad a disminuir | ❌ No | ≥1 |
| `reason` | `str` | Explicación de la reducción | ✔️ Sí | - |

### 🔄 Flujo de Ejecución  

1. **Protección de Valor Mínimo**  
   - Asegura que el renombre nunca baje de 1:  
     ```python 
     player.renombre = max(1, player.renombre - amount)
     ```

2. **Registro Condicional**  
   - Si hay `reason` y el jugador tiene partidos asociados:  
     - Busca su último partido (`match_set.order_by('-scheduled_at').first()`).  
     - Crea un log usando `create_match_log` con el formato:  
       ```python
       f"Renombre reducido en {amount} por: {reason}"
       ```

3. **Retorno**  
   - Devuelve la instancia del jugador (actualizada o sin cambios si ya tenía renombre ≤1).

### ⚠️ Restricciones Clave  

- **Límite inferior**: El renombre nunca será menor que 1.  
- **Dependencias**:  
  - Requiere relación `match_set` en el modelo `Player`.  
  - Asume existencia de `create_match_log`.  

```python
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

    return player
```
---

## 🏅 Función `increase_player_renombre`

### 📌 Descripción  
Incrementa el renombre de un jugador con un límite máximo de 100, registra el evento en un log si se proporciona una razón válida y devuelve el jugador actualizado.

---

### 📋 Parámetros  

| Parámetro | Tipo | Descripción | Opcional | Restricciones |
|-----------|------|-------------|----------|---------------|
| `player` | `Player` | Jugador afectado | ❌ No | - |
| `amount` | `int` | Cantidad a incrementar | ❌ No | ≥1 |
| `reason` | `str` | Motivo del aumento | ✔️ Sí | - |

---

### 🔄 Flujo de Ejecución  

1. **Protección de Valor Máximo**  
   - Asegura que el renombre nunca exceda 100:  
     ```python 
     player.renombre = min(100, player.renombre + amount)
     ```

2. **Registro Condicional**  
   - Si existe `reason` y el jugador tiene partidos asociados:  
     - Busca su último partido (`match_set.order_by('-scheduled_at').first()`).  
     - Crea un log con el formato:  
       ```python
       f"Renombre incrementado en {amount} por: {reason}"
       ```

3. **Retorno**  
   - Devuelve la instancia del jugador (actualizada o sin cambios si ya tenía renombre ≥100).

---

### ⚠️ Restricciones Clave  

- **Límite superior**: El renombre nunca superará 100.  
- **Dependencias**:  
  - Requiere relación `match_set` en el modelo `Player`.  
  - Asume existencia de `create_match_log`.  

```python
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

    return player

```
---

## 🏅 Función `process_final_match`

### 📌 Descripción  
Procesa la finalización de un torneo cuando se completa el último partido, determinando al ganador, actualizando el estado del torneo y distribuyendo recompensas a los jugadores del equipo ganador.

### 📋 Parámetros  
| Parámetro | Tipo | Descripción |  
|-----------|------|-------------|  
| `tournament` | `Tournament` | Instancia del torneo a finalizar |  
| `completed_matches_queryset` | `QuerySet` | Conjunto de partidos completados (debe estar ordenado cronológicamente) |  

### 🔄 Flujo de Ejecución  

1. **Determinación del Ganador**  
- Obtiene el último partido completado usando `.first()`  
- Verifica que exista un ganador en ese partido  

2. **Actualización del Torneo**  
- En una transacción atómica:  
  - Asigna el ganador al torneo  
  - Cambia el estado a 'completed'  
  - Guarda los cambios  

3. **Distribución de Recompensas**  
- Si existe `prize_pool`:  
  - Divide el monto equitativamente entre todos los jugadores del equipo ganador  
  - Jugadores Premium reciben el doble  
  - Actualiza el saldo de `coins` de cada jugador  

4. **Notificaciones**  
- Envía un email a cada jugador del equipo ganador notificando la victoria  

## ⚠️ Casos Especiales  
- Si no hay jugadores en el equipo ganador, omite la distribución de premios  

```python
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

```
---
## 🏅 Función `process_round`

### 📌 Descripción  
Gestiona la transición entre rondas en un torneo, procesando los resultados de la ronda anterior y generando los nuevos enfrentamientos para la siguiente fase competitiva. La función actúa como puente lógico entre etapas del torneo.

### 📋 Parámetros  

| Parámetro | Tipo | Descripción | Requisitos |
|-----------|------|-------------|------------|
| `tournament` | `Tournament` | Torneo activo | Debe existir en BD |
| `round_number` | `int` | Número de ronda actual | > 1 |

### 🔄 Flujo de Ejecución  

1. **Fase de Recolección**  
- Identifica todos los partidos completados de la ronda anterior  
- Filtra y almacena exclusivamente los equipos ganadores válidos  
- Descarta automáticamente partidos sin ganador definido  

2. **Fase de Validación**  
- Verifica cantidad mínima de equipos (≥2)  
- Confirma paridad en número de equipos (2,4,8...)  
- Evalúa condiciones para continuar el torneo  

3. **Fase de Emparejamiento**  
- Ordena equipos por rendimiento (MMR ascendente)  
- Establece parejas competitivas:  
  - Mejor rendimiento vs segundo mejor  
  - Tercero vs cuarto  
  - [...]  

4. **Fase de Generación**  
- Crea nuevos registros de partidos en base de datos  
- Configura automáticamente:  
  - Fechas/horas (5 minutos tras generación)  
  - Estado inicial "pendiente"  
  - Relaciones torneo-equipos  

5. **Fase de Confirmación**  
- Actualiza metadatos del torneo  
- Genera logs detallados de la operación  
- Proporciona feedback visual en consola  

```python
def process_round(tournament, round_number):
    """
    Procesa la generación de partidos para la siguiente ronda de un torneo,
    utilizando los equipos ganadores de la ronda anterior.

    Args:
        tournament (Tournament): Instancia del torneo en curso.
        round_number (int): Número de la ronda a procesar (por ejemplo, 2 para la segunda ronda).

    Return:
        None
    """
    # Obtener los partidos completados de la ronda anterior
    previous_round = round_number - 1
    completed_matches_queryset = Match.objects.filter(
        tournament=tournament,
        round=previous_round,
        winner__isnull=False
    )

    # Obtener los IDs de los equipos ganadores
    winner_team_ids = [match.winner.id for match in completed_matches_queryset]

    # Obtener los TournamentTeam correspondientes a los equipos ganadores
    winning_tournament_teams = TournamentTeam.objects.filter(
        tournament=tournament,
        team__id__in=winner_team_ids
    )

    # Validar que haya suficientes equipos (en número par) para emparejar
    if winning_tournament_teams.count() >= 2 and winning_tournament_teams.count() % 2 == 0:
        # Generar los partidos para la siguiente ronda usando los TournamentTeam ganadores
        generate_matches_by_mmr(tournament.id, round=round_number, tournament_teams=winning_tournament_teams)
```
---

## 🔄 Navegación

- ️🏗️ [Estructura del Proyecto y esquema de base de datos](PROJECT_STRUCTURE.md)
- ⚙️ [Admin](ADMIN.md)
- 🖼️ [Vistas](VIEWS.md)
- ⏰ [Tareas programadas](TASKS.md)
- 🧩 [Modelos](MODELS.md)
- 📝 [Formularios](FORMS.md)
- ✅ [Test](TESTS.md)
- 🔄 [Serializadores](SERIALIZERS.md)
- 🧠 [Funciones](FUNCTIONS.md)
- 🎯 [Workflows](WORKFLOWS.md)
- 🚀 [Compose](DOCKER-COMPOSE.md)
- ⬅️ [Volver al README principal](../README.md)
