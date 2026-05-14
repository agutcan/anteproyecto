# 🚀 Workflow de Despliegue en Docker & AWS

## 📋 Visión General
Este proyecto cuenta con dos flujos de trabajo automatizados:

1. **docker_aws.yml**: Despliegue de la aplicación principal Django en AWS
2. **subirEC2-documents.yml**: Actualización de documentos y reconstrucción del microservicio de soporte IA

---

## 🔄 Workflow 1: Despliegue Principal (docker_aws.yml)

### 📌 Visión General
Automatiza el proceso completo de construcción, publicación y despliegue de la aplicación en infraestructura AWS.

## 🎯 Condiciones de Activación
- **Rama**: Solo se ejecuta en la rama main
- **Rutas**: Se activa únicamente con cambios en:
  - Directorios de código de la aplicación
  - Archivos de plantillas
  - Archivos de configuración de Docker
  - Requerimientos de Python
   - Configuración de formato (`pyproject.toml`)
   - Definiciones de workflows (`.github/workflows/**`)

## ⚙️ Variables de Entorno
| Variable | Valor | Descripción |
|----------|-------|-------------|
| `IMAGE_NAME` | anteproyecto | Nombre de la imagen Docker |
| `IMAGE_TAG` | latest | Tag de la imagen |
| `COMPOSE` | docker-compose.yml | Archivo de composición |

## 🔄 Proceso de Ejecución

### 1. 🎨 Validación de formato con Black
**Pasos:**
1. Checkout del código
2. Configuración de Python 3.13
3. Instalación de dependencias (`requirements.txt`)
4. Ejecución de `python -m black --check .`

### 2. 🏗️ Construcción de Imagen Docker
**Pasos:**
1. Checkout del código
2. Login en Docker Hub usando credenciales secretas
3. Construcción y publicación de la imagen con el formato: `usuario/anteproyecto:latest`

### 3. 🚀 Despliegue en AWS
**Requisito:** Depende de la finalización exitosa de los jobs de formato y construcción

**Pasos:**
1. Conexión SSH a la instancia AWS usando:
   - Hostname
   - Usuario
   - Clave privada
   - Puerto
   (Todos almacenados en GitHub Secrets)

2. Secuencia de comandos de despliegue:
   - Navegación al directorio de la aplicación
   - Actualización del código (git pull)
   - Detención de contenedores existentes
   - Eliminación de imágenes antiguas
   - Descarga de la nueva imagen
   - Inicio de los contenedores en modo detached

## 🔒 Consideraciones de Seguridad
- Todas las credenciales sensibles se almacenan en GitHub Secrets
- La conexión a AWS utiliza autenticación por SSH con clave privada
- El workflow solo se activa en la rama principal

## ⏱️ Frecuencia de Ejecución
El workflow se ejecuta automáticamente con cada:
- Push a la rama main
- Pull request hacia la rama main
(Solo cuando hay cambios en los archivos/directorios monitoreados)

## 📊 Beneficios Clave
- **Automatización completa** del proceso de despliegue
- **Consistencia** al usar siempre la misma versión (latest)
- **Eficiencia** al eliminar imágenes antiguas
- **Seguridad** mediante el uso de secrets
- **Rapidez** en el proceso de actualización

---

## 🔄 Workflow 2: Actualización de Documentos subirEC2 (subirEC2-documents.yml)

### 📌 Visión General
Automatiza la actualización de documentos en el microservicio de soporte IA cuando hay cambios en `subirEC2/documents/`.

### 🎯 Condiciones de Activación
- **Rama**: Solo se ejecuta en la rama main
- **Rutas**: Se activa únicamente con cambios en:
  - `subirEC2/documents/**`
- **Eventos**: Push y Pull Requests a la rama main

### ⚙️ Pasos de Ejecución
1. **Checkout del código** (implícito)
2. **Conexión SSH a EC2** usando credenciales secretas:
   - `AWS_HOSTNAME2`: Dirección IP/dominio de la instancia EC2
   - `AWS_USERNAME`: Usuario SSH (ubuntu)
   - `AWS_PRIVATEKEY`: Clave privada SSH
   - `PORT`: Puerto SSH

3. **Secuencia de comandos remotos**:
   ```bash
   cd /home/ubuntu/anteproyecto/subirEC2
   source .venv/bin/activate
   git pull
   python -m app.ingest  # Reindexar documentos
   docker compose down -v  # Detener y eliminar volúmenes
   docker compose up -d --build  # Reconstruir y reiniciar servicios
   ```

### 🎯 Propósito
- Actualizar la base documental del RAG (Retrieval Augmented Generation)
- Reindexar documentos para búsqueda semántica
- Reiniciar los contenedores con la nueva configuración
- Garantizar que el chatbot de soporte tenga los documentos más actualizados

### 📄 Documentos Procesados
El microservicio indexa archivos Markdown en `subirEC2/documents/`:
- `guia_usuario.md`: Guía de uso general
- `torneos.md`: Información sobre torneos
- `equipos.md`: Información sobre equipos
- `perfil_y_estadisticas.md`: Perfiles y estadísticas
- `recompensas_y_premium.md`: Sistema de recompensas
- `politicas.md`: Políticas de plataforma
- `soporte_y_contacto.md`: Información de soporte
- `support_faq.md`: Preguntas frecuentes

### 🔗 Relación con subirEC2
El microservicio `subirEC2`:
- Ejecuta FastAPI para exponer un endpoint `/api/support/chat/`
- Utiliza embeddings (local o cloud) para búsqueda semántica
- Integra con LLMs (OpenAI, Anthropic, Groq, Ollama)
- Almacena índices en `subirEC2/data/`

### 🔒 Consideraciones de Seguridad
- Las credenciales SSH se almacenan en GitHub Secrets
- El workflow es de solo lectura (git pull, no push)
- Solo se ejecuta en la rama main
- Utiliza acceso SSH con clave privada

## 📊 Beneficios Clave
- **Automatización completa** del proceso de despliegue
- **Consistencia** al usar siempre la misma versión (latest)
- **Eficiencia** al eliminar imágenes antiguas
- **Seguridad** mediante el uso de secrets
- **Rapidez** en el proceso de actualización

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
