# 🚀 Documentación del Docker Compose para ArenaGG

## 🌐 Arquitectura de Servicios

### 🔒 Traefik (Reverse Proxy)
- **Imagen**: `traefik:v3.2`
- **Funcionalidades**:
  - Dashboard administrativo habilitado
  - Redirección HTTP → HTTPS automática
  - Certificados SSL con Let's Encrypt
  - Autenticación básica para el dashboard
- **Puertos expuestos**: 80, 443, 8080
- **Volúmenes**:
  - Certificados Let's Encrypt
  - Socket de Docker

### 🖥️ Servicio Web (Django)
- **Configuración**:
  - Servido con Gunicorn (4 workers + 2 threads)
  - Variables de entorno desde `.env`
  - Volúmenes para archivos estáticos y media
- **Routing**:
  - Disponible en `arenagg.aarongutierrez.tech`
  - Balanceador de carga en puerto 8000

### 🗃️ Base de Datos (PostgreSQL)
- **Imagen**: `postgres:16`
- **Persistencia**:
  - Volumen dedicado para datos
  - Configuración desde variables de entorno
- **Política de reinicio**: unless-stopped

### 📧 Mailpit (Servidor SMTP de prueba)
- **Características**:
  - Interfaz web en `mailpit.aarongutierrez.tech`
  - Puerto SMTP en 1025
  - Panel web en 8025
- **Almacenamiento**: Directorio local ./data

### 🟥 Redis
- **Uso**: Broker para Celery
- **Imagen**: `redis:7`

### 🎯 Celery
- **Workers**: Configurados con loglevel info
- **Dependencias**: Requiere servicios web y redis

### ⏱️ Celery Beat
- **Función**: Programador de tareas
- **Scheduler**: DatabaseScheduler

### 🖼️ Servidor de Medios (Nginx)
- **Propósito**: Servir archivos multimedia
- **Configuración**:
  - Ruta `/media` en el mismo dominio principal
  - Volumen de solo lectura

## 🔐 Seguridad

| Componente | Medida de Seguridad |
|------------|---------------------|
| Traefik | HTTPS obligatorio |
| Dashboard | Autenticación básica |
| Certificados | Auto-renovación Let's Encrypt |
| DB | Volumen persistente |

## 🔗 URLs de Acceso

| Servicio            | URL                                                |
|---------------------|-----------------------------------------------------|
| Aplicación          | [https://arenagg.aarongutierrez.tech](https://arenagg.aarongutierrez.tech) |
| Mailpit             | [https://mailpit.aarongutierrez.tech](https://mailpit.aarongutierrez.tech) |
| Traefik Dashboard   | [https://aarongutierrez.tech](https://aarongutierrez.tech) |

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
