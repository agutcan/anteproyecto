# 🚀 Workflow de Despliegue en Docker & AWS

## 📋 Visión General
Este flujo de trabajo automatiza el proceso completo de construcción, publicación y despliegue de la aplicación en infraestructura AWS.

## 🎯 Condiciones de Activación
- **Rama**: Solo se ejecuta en la rama main
- **Rutas**: Se activa únicamente con cambios en:
  - Directorios de código de la aplicación
  - Archivos de plantillas
  - Archivos de configuración de Docker
  - Requerimientos de Python

## ⚙️ Variables de Entorno
| Variable | Valor | Descripción |
|----------|-------|-------------|
| `IMAGE_NAME` | anteproyecto | Nombre de la imagen Docker |
| `IMAGE_TAG` | latest | Tag de la imagen |
| `COMPOSE` | docker-compose.yml | Archivo de composición |

## 🔄 Proceso de Ejecución

### 1. 🏗️ Construcción de Imagen Docker
**Pasos:**
1. Checkout del código
2. Login en Docker Hub usando credenciales secretas
3. Construcción y publicación de la imagen con el formato: `usuario/anteproyecto:latest`

### 2. 🚀 Despliegue en AWS
**Requisito:** Depende de la finalización exitosa del job de construcción

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
