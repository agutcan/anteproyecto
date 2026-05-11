# Torneos

## Flujo basico

1. Se crea el torneo.
2. Los equipos se inscriben.
3. El torneo pasa a estado visible `En progreso` cuando llega su fecha de inicio.
4. Se generan los enfrentamientos.
5. Los equipos confirman que estan listos.
6. Se registra el resultado de cada partida.
7. El torneo termina cuando queda un ganador.

## Como funciona la inscripcion

Un torneo guarda el numero maximo de equipos y el numero maximo de jugadores por equipo.

Para poder entrar:

- el equipo debe cumplir el numero de jugadores,
- el torneo no puede estar cerrado,
- el formato debe ser compatible con el sistema.

## Formato de eliminatorias

ArenaGG trabaja con torneos de:

- 2 equipos,
- 4 equipos,
- 8 equipos.

## Estados visibles del torneo

En la interfaz el torneo se muestra con estos estados:

- `Inscripciones abiertas`: el torneo todavía acepta equipos.
- `En progreso`: el torneo ya ha comenzado.
- `Finalizado`: el torneo terminó y ya tiene ganador.

## Estados de una partida

- `Pendiente`: pendiente de comenzar.
- `En juego`: la partida está activa.
- `Finalizada`: la partida terminó.

## Confirmacion de partidas

Antes de jugar, cada equipo puede marcar que esta listo.

Si ambos equipos estan listos, la partida puede empezar.

Si llega la hora y un equipo no se presenta, el sistema puede decidir un ganador segun las reglas internas.

## Logros visibles para el jugador

El usuario puede consultar:

- detalles del torneo,
- detalles de la partida,
- logs del torneo,
- resultados finales.
