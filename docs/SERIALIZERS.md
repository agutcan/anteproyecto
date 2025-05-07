# Explicación de Serializers en Django (`serializers.py`)

Este archivo define los serializadores utilizados en la aplicación web. Los serializadores representan la forma en que los datos del backend, se transforman en formatos que pueden ser enviados o recibidos a través de una API, como JSON o XML. A continuación, se describen cada uno de los serializadores:

---

## TournamentSerializer

### Descripción
Serializador para el modelo `Tournament` que adapta los nombres de campos para su uso en interfaces frontend, en mi caso un calendario.

### Propósito
Transforma la estructura de datos del modelo Tournament para:
1. Adaptar nombres de campos a convenciones frontend
2. Formatear fechas para compatibilidad con librerías JavaScript
3. Seleccionar campos específicos para la API pública

### Transformaciones de Campos

| Campo Modelo | Campo Serializado | Tipo | Formato | Descripción |
|-------------|------------------|------|---------|-------------|
| name | title | CharField | - | Nombre público del torneo |
| start_date | start | DateTimeField | %Y-%m-%dT%H:%M:%S | Fecha de inicio en formato ISO 8601 |

### Campos Incluidos

1. **id**  
   - Tipo: Integer (automático)  
   - Descripción: Identificador único del torneo

2. **title**  
   - Tipo: CharField  
   - Origen: Campo `name` del modelo  
   - Uso: Nombre legible para mostrar en UI

3. **game**  
   - Tipo: Relación (ForeignKey)  
   - Descripción: Juego asociado al torneo

4. **start**  
   - Tipo: DateTimeField  
   - Formato: `YYYY-MM-DDTHH:MM:SS` (ISO 8601)  
   - Ejemplo: `2023-05-15T14:30:00`

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

## 🔄 Navegación
[⬅️ Volver al README principal](../README.md)
