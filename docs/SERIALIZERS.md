 # 🏆 Explicación de Serializers en Django (`serializers.py`)

Este archivo define los serializadores utilizados en la aplicación web. Los serializadores representan la forma en que los datos del backend, se transforman en formatos que pueden ser enviados o recibidos a través de una API, como JSON o XML. A continuación, se describen cada uno de los serializadores:

---
<!--
## 🏅 TournamentSerializer


### 📝 Descripción
Serializador para el modelo `Tournament` que adapta los nombres de campos para su uso en interfaces frontend, en mi caso un calendario.

### 🎯 Propósito
Transforma la estructura de datos del modelo Tournament para:
1. 🔄 Adaptar nombres de campos a convenciones frontend
2. ⏱️ Formatear fechas para compatibilidad con librerías JavaScript
3. 🎯 Seleccionar campos específicos para la API pública

### 🔧 Transformaciones de Campos 

| Campo Modelo | Campo Serializado | Tipo | Formato | Descripción |
|-------------|------------------|------|---------|-------------|
| name | title | CharField | - | Nombre público del torneo |
| start_date | start | DateTimeField | %Y-%m-%dT%H:%M:%S | Fecha de inicio en formato ISO 8601 |

### 📌 Campos Incluidos 

1. **id**  
   - 🏷️ Tipo: Integer (automático)  
   - 📄 Descripción: Identificador único del torneo

2. **title**  
   - 🏷️ Tipo: CharField  
   - 📄 Uso: Nombre legible para mostrar en UI

3. **game**  
   - 🏷️ Tipo: Relación (ForeignKey)  
   - 📄 Descripción: Juego asociado al torneo

4. **start**  
   - 🏷️ Tipo: DateTimeField  
   - 📅 Formato: `YYYY-MM-DDTHH:MM:SS` (ISO 8601)  
   - 📝 Ejemplo: `2023-05-15T14:30:00`

```python
class TournamentSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Tournament que adapta los nombres de campos
    para su uso en interfaces frontend.

    Transformaciones:
    - Campo 'name' del modelo → se expone como 'title'
    - Campo 'start_date' del modelo → se expone como 'start' en formato ISO 8601

    Campos incluidos:
    - id: Identificador único del torneo
    - title: Nombre del torneo (mapeado desde 'name')
    - game: Juego asociado al torneo
    - start: Fecha de inicio en formato YYYY-MM-DDTHH:MM:SS
    """
    
    title = serializers.CharField(
        source='name',
    )
    
    start = serializers.DateTimeField(
        source='start_date',
        format='%Y-%m-%dT%H:%M:%S',
    )

    class Meta:
        model = Tournament
        fields = ["id", "title", "game", "start"]
```
-->
## 🎮 PlayerStatsSerializer

### 📝 Descripción
Serializador para estadísticas públicas de jugadores que expone métricas clave de rendimiento.

### 🎯 Propósito
Proporciona una vista estructurada de:
1. 👤 Identificación básica del jugador
2. 🏆 Estadísticas competitivas
3. 📊 Datos calculados de rendimiento

### 📌 Campos Incluidos

1. **username**  
   - 🏷️ Tipo: CharField  
   - 📄 Descripción: Nombre público del jugador  
   - 🔒 Acceso: Solo lectura  

2. **games_won**  
   - 🏷️ Tipo: IntegerField  
   - 📄 Descripción: Número total de partidas ganadas  
   - ✅ Validación: Valor positivo o cero  

3. **winrate**  
   - 🏷️ Tipo: FloatField  
   - 📄 Descripción: Porcentaje de victorias (rango 0-100)  
   - 🔢 Formato: Decimal con 1 dígito (ej: 72.5)  

```python
class PlayerStatsSerializer(serializers.ModelSerializer):
    """Serializador para estadísticas públicas de jugadores
    
    Atributos expuestos:
        username (str): Nombre de usuario obtenido del modelo User relacionado
        games_won (int): Número total de partidas ganadas
        winrate (float): Porcentaje de victorias (0-100)
    
    Uso típico:
        - Tablas de clasificación
        - Perfiles públicos de jugadores
        - Componentes de estadísticas
    """
    username = serializers.CharField(
        source='user.username',
    )

    class Meta:
        model = Player
        fields = ['username', 'games_won', 'winrate']
```

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

---

## 🔔 Nota sobre `NotificationSerializer`

El proyecto incorporó `NotificationSerializer` para exponer las notificaciones del usuario en la API del frontend.

### Campos principales
- `id`, `title`, `message`, `urgency`, `status`
- `created_at`, `read_at`
- `sender_email`
- `recipients`

### Uso
- Alimenta `/api/notifications/`
- Se usa en la barra superior para el panel de notificaciones
- Mantiene el filtrado por usuario autenticado