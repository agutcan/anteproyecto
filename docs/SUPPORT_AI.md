# Soporte IA de ArenaGG

Este documento explica como se ha montado el asistente de soporte de la aplicacion, que se ejecuta en el microservicio `subirEC2` y que responde a las dudas de usuarios normales sobre ArenaGG.

## 1. Objetivo

El asistente de soporte se creo para responder preguntas frecuentes de la aplicacion, por ejemplo:

- como me registro,
- como inicio sesion,
- como me uno a un torneo,
- como creo o abandono un equipo,
- como veo mi perfil y mis estadisticas,
- como canjeo recompensas,
- como funciona Premium,
- cuando debo contactar con soporte humano.

La idea es que el bot responda con informacion real de la documentacion, no con respuestas inventadas.

## 2. Arquitectura general

La solucion esta dividida en dos partes:

1. **Django ArenaGG**: la aplicacion principal que ve el usuario.
2. **subirEC2**: microservicio FastAPI encargado del chat de soporte.

El flujo real es este:

1. El usuario escribe una duda en la seccion de soporte de Django.
2. La vista `web.views.support_chat_api` envia el mensaje al microservicio `subirEC2`.
3. `subirEC2` busca el contexto relevante en la base documental.
4. El proveedor LLM genera la respuesta final.
5. Django normaliza la respuesta y la muestra en pantalla.

## 3. Como funciona la API de soporte

El microservicio expone tres endpoints principales:

- `GET /health`: comprueba que el servicio esta levantado.
- `POST /chat`: recibe la pregunta del usuario y devuelve la respuesta.
- `POST /reindex`: reconstruye el indice vectorial con los documentos de soporte.

### 3.1 `/health`

Devuelve el estado del servicio, el proveedor activo y el modelo configurado.

### 3.2 `/chat`

Recibe un JSON con una pregunta, por ejemplo:

```json
{
  "question": "Como me uno a un torneo?"
}
```

La respuesta incluye:

- `answer`: respuesta generada.
- `confidence`: puntuacion de recuperacion.
- `should_escalate`: indica si el caso debe pasar a una persona.
- `sources`: archivos que se usaron como contexto.

### 3.3 `/reindex`

Sirve para regenerar el indice cuando cambian los documentos de soporte. Esta protegido con `X-Admin-Token`.

## 4. Documentacion que usa el bot

El microservicio indexa los archivos Markdown y texto que hay en `subirEC2/documents`.

Esa carpeta contiene una base de conocimiento pensada para usuarios normales, con temas como:

- registro e inicio de sesion,
- torneos,
- equipos,
- perfil y estadisticas,
- recompensas y Premium,
- soporte y contacto.

El indice se genera a partir de esos documentos y se guarda en `subirEC2/data`.

## 5. Flujo RAG

El bot sigue un flujo de recuperacion y generacion:

1. Lee los documentos de `subirEC2/documents`.
2. Los divide en fragmentos mas pequeños.
3. Convierte cada fragmento en vectores con un modelo de embeddings.
4. Guarda el indice en FAISS.
5. Cuando llega una pregunta, busca los fragmentos mas cercanos.
6. Con ese contexto llama al proveedor LLM.
7. Devuelve la respuesta final con las fuentes usadas.

## 6. Proveedores LLM

La capa LLM admite estos proveedores:

- `openai`
- `mistral`
- `together`
- `bedrock`

La seleccion se hace desde variables de entorno en `subirEC2/.env`.

## 7. Integracion con Django

La vista `web.views.support_chat_api` hace de proxy entre la web principal y el microservicio.

El valor habitual para conectar la app principal con el bot es:

```bash
SUPPORT_AI_API_URL=http://127.0.0.1:8081/chat
```

Esto permite que la pagina de soporte de Django use la API de `subirEC2` sin que el usuario vea la complejidad interna.

## 8. Despliegue en AWS

El despliegue se pensó para una instancia EC2 pequeña, con la API corriendo en localhost y un proxy inverso delante.

### 8.1 Recursos usados

- **EC2**: servidor donde se ejecuta el microservicio.
- **Security Group**: abre solo los puertos necesarios.
- **Dominio publico**: apunta al servidor EC2.
- **Nginx o proxy inverso**: publica la API en HTTPS.
- **Let’s Encrypt**: emite el certificado TLS.

### 8.2 Esquema de despliegue

La arquitectura final es esta:

1. Internet accede al dominio publico `api.arenagg.tech`.
2. Nginx recibe el trafico HTTPS.
3. Nginx reenvia las peticiones a `127.0.0.1:8081`.
4. El proceso FastAPI responde la solicitud.
5. Django consume esa URL desde su propia configuracion.

### 8.3 Motivo de usar localhost

La API no se expone directamente a Internet. Se publica solo en `127.0.0.1:8081` para dejar el control de HTTPS y del dominio al proxy inverso.

## 9. Archivo de despliegue

En `subirEC2` se usan estos archivos principales:

- `Dockerfile`: construye la imagen del servicio.
- `docker-compose.yml`: expone la API solo en localhost.
- `.env`: configura proveedor, clave y rutas.
- `requirements.txt`: dependencias Python.

## 10. Reindexado en produccion

Cuando cambian los documentos de soporte, hay que volver a indexar.

El proceso normal es:

```bash
cd subirEC2
python -m app.ingest
```

Si el servicio esta en Docker, tambien se puede ejecutar dentro del contenedor.

## 11. Permisos y almacenamiento

El indice necesita poder escribirse en `subirEC2/data`.

Si aparece un error de permisos, hay que revisar:

- propietario de la carpeta,
- permisos de escritura,
- usuario con el que corre el servicio.

## 12. Que ve el usuario final

El usuario no interactua con FAISS, ni con embeddings, ni con el proveedor LLM.

Solo ve una ventana de soporte que responde preguntas frecuentes de la aplicacion con un lenguaje simple y orientado a usuarios normales.

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
