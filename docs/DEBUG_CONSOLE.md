# 🔧 Debug Console - Consola Interactiva de Depuración

## Descripción General

La **Debug Console** es una herramienta administrativa para ejecutar consultas ORM (Django) directamente desde el navegador durante el desarrollo. Permite a los administradores inspeccionar y manipular datos de la base de datos sin necesidad de acceder a la terminal.

## Características

- ✅ Ejecución de consultas ORM Python/Django
- ✅ Modo `eval()` para obtener resultados de expresiones
- ✅ Modo `exec()` para ejecutar sentencias
- ✅ Historial de consultas con navegación (↑ ↓)
- ✅ Output formateado con colores según el resultado
- ✅ Interfaz elegante tipo "dev tools"
- ✅ Seguridad integrada: solo para admins, validación de keywords peligrosos

## Cómo Usar

### 1. Abrir la Consola

Presiona **F12** en cualquier página del sitio web (solo visible para administradores).

```
F12 → Abre/Cierra la consola
Escape → Cierra la consola
```

### 2. Escribir Consultas

En el textarea de "Consulta ORM", ingresa consultas Python/Django válidas.

**Modo Eval (✓ checkbox activado):**
```python
# Devuelve el resultado de la expresión
list(Player.objects.filter(country='ES').values('user__username', 'mmr')[:5])

# Contar jugadores por país
Player.objects.values('country').annotate(count=Count('id'))

# Buscar torneos específicos
list(Tournament.objects.filter(status='ongoing').values('name', 'max_teams'))
```

**Modo Exec (✗ checkbox desactivado):**
```python
# Ejecutar código sin retornar resultado
player = Player.objects.get(user__username='testuser')
player.mmr = 2000
player.save()
```

### 3. Ejecutar

- **Botón "Ejecutar"** o **Ctrl+Enter**: Ejecuta la consulta
- **Botón "Limpiar Output"**: Borra los resultados previos

### 4. Ver Resultados

Los resultados aparecen en el área "Resultado" con:
- ✅ **Verde (success)**: Consulta ejecutada correctamente
- ❌ **Rojo (error)**: Error en la sintaxis o en la ejecución

## Contexto Disponible

La siguiente tabla muestra los modelos y funciones disponibles en el contexto de ejecución:

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `Player` | Model | Modelo de jugadores |
| `User` | Model | Modelo de usuarios (Django) |
| `Team` | Model | Modelo de equipos |
| `Tournament` | Model | Modelo de torneos |
| `Match` | Model | Modelo de partidos |
| `MatchResult` | Model | Modelo de resultados de partidos |
| `MatchLog` | Model | Modelo de eventos/logs de partidos |
| `Game` | Model | Modelo de juegos |
| `Reward` | Model | Modelo de recompensas |
| `Redemption` | Model | Modelo de canjes de recompensas |
| `TournamentTeam` | Model | Modelo de equipos en torneos |
| `Notification` | Model | Modelo de notificaciones |
| `Q` | Function | Q objects para consultas complejas |
| `F` | Function | F expressions para operaciones de campos |
| `Count` | Function | Agregación Count para consultas |

## Ejemplos Prácticos

### Ejemplo 1: Listar jugadores de un país

```python
# Modo eval
list(Player.objects.filter(country='ES').values('user__username', 'country'))
```

**Resultado esperado:**
```
[
  {'user__username': 'jugador1', 'country': 'ES'},
  {'user__username': 'jugador2', 'country': 'ES'}
]
```

### Ejemplo 2: Contar torneos por estado

```python
# Modo eval
list(Tournament.objects.values('status').annotate(count=Count('id')))
```

**Resultado:**
```
[
  {'status': 'upcoming', 'count': 5},
  {'status': 'ongoing', 'count': 2},
  {'status': 'completed', 'count': 12}
]
```

### Ejemplo 3: Obtener ranking top 5

```python
# Modo eval
list(Player.objects.order_by('-mmr').values('id', 'mmr')[:5])
```

### Ejemplo 4: Actualizar MMR de un jugador (Modo exec)

```python
# Modo exec - No devuelve resultado, pero modifica BD
player = Player.objects.get(id=1)
player.mmr = 2500
player.save()
```

### Ejemplo 5: Contar equipos por jugador

```python
# Modo eval
list(Team.objects.values('name').annotate(players=Count('player')))
```

### Ejemplo 6: Buscar partidos ganados por un equipo

```python
# Modo eval
list(Match.objects.filter(winner__name='TeamA').values('tournament__name', 'scheduled_at'))
```

## Navegación del Historial

Usa las **flechas del teclado** en el textarea para navegar por consultas anteriores:

- **↑ (Arriba)**: Muestra la consulta anterior
- **↓ (Abajo)**: Muestra la siguiente consulta

## Restricciones de Seguridad

La consola rechaza consultas que contengan:

- `__import__` - Importar módulos dinámicos
- `exec(` - Ejecutar código adicional desde dentro de exec
- `eval(` - Ejecutar código adicional desde dentro de eval
- `open(` - Acceder al sistema de archivos
- `subprocess` - Ejecutar comandos del sistema
- `os.` - Operaciones del sistema operativo
- `system(` - Llamadas al sistema

**Mensaje de error si intenta algo peligroso:**
```
La consulta contiene palabras clave prohibidas por razones de seguridad.
```

## Logging

Todas las consultas ejecutadas se registran en los logs de Django (`logs/django.log` si está configurado):

```
[INFO] Debug query (eval) ejecutado por admin: Player.objects.all()
[ERROR] Syntax error en debug query de admin: invalid syntax
```

## Acceso y Permisos

### Solo para Administradores

- **Visibilidad**: El CSS y JS solo se cargan para usuarios con `user.is_staff=True`
- **API**: El endpoint `/api/debug/query/` devuelve **403 Forbidden** para usuarios no-admin
- **Restricción en BD**: Usa decorador `@permission_classes([IsAuthenticated])` + verificación `if not request.user.is_staff`

**Crear un usuario administrador** (si no tienes uno):

```bash
python manage.py createsuperuser
```

## Estructura Técnica

### Backend

**Endpoint**: `POST /api/debug/query/`

**Solicitud:**
```json
{
    "query": "Player.objects.filter(country='ES').values('id')",
    "eval": true
}
```

**Respuesta (éxito):**
```json
{
    "success": true,
    "result": "[{'username': 'player1'}, {'id': 'player2'}]"
}
```

**Respuesta (error):**
```json
{
    "success": false,
    "error": "SyntaxError: invalid syntax"
}
```

### Frontend

**Archivo JS**: `web/static/js/debug_console.js`
- Clase `DebugConsole` que gestiona la UI y las solicitudes
- Soporte para historial de consultas
- Auto-scroll en el área de output

**Archivo CSS**: `web/static/css/debug_console.css`
- Estilos inspirados en Developer Tools
- Tema oscuro para menor fatiga visual
- Responsive design para dispositivos móviles

**Template Base**: `web/templates/base.html`
- Condicional `{% if user.is_staff %}` para cargar los archivos
- Solo se incluyen para admins

### Vista Django

**Archivo**: `web/views.py`

**Función**: `debug_query_api()`
- Verifica permiso de staff
- Valida la consulta (busca keywords peligrosas)
- Ejecuta con `eval()` o `exec()` según el flag
- Captura excepciones y devuelve mensajes de error amigables

## Troubleshooting

### La consola no aparece

**Verificar:**
1. ¿Estás logueado como administrador?
2. Abre la consola del navegador (F12 nativo) y verifica que no hay errores JavaScript

### Error "403 Forbidden"

Tu usuario no es administrador. Pide a un superusuario que:
```bash
python manage.py shell
from django.contrib.auth.models import User
user = User.objects.get(username='tu_usuario')
user.is_staff = True
user.is_superuser = True
user.save()
```

### Consulta devuelve "query execution timed out"

La consulta toma mucho tiempo. Intenta:
- Limitar el resultado con `.count()` primero
- Usar `.first()` en lugar de `.all()`
- Verificar que existen índices en la BD para campos consultados

### No veo cambios en BD tras ejecutar una consulta

**Modo Exec no ejecuta `.save()`:**
```python
# Esto NO funciona automáticamente
player.mmr = 5000  # No se guarda

# Esto SÍ funciona:
player.mmr = 5000
player.save()
```

## Notas Importantes

1. **Seguridad**: Los logs guardan quién ejecutó cada consulta - úsalo responsablemente
2. **Datos**: Cualquier modificación a la BD es real - ¡ten cuidado con updates!
3. **Performance**: Consultas muy complejas pueden bloquear el servidor brevemente

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
- 🤖 [Soporte IA](SUPPORT_AI.md)
- ☁️ [Despliegue del soporte en AWS](SUPPORT_AI_AWS.md)
- 🔧 [Debug Console](DEBUG_CONSOLE.md)
- ⬅️ [Volver al README principal](../README.md)