# Memoria de Uso de Contenedores en el Desarrollo

## 1. Introducción y contextualización

El proyecto desarrollado ha sido ArenaGG, una plataforma web orientada a la organización y gestión de torneos de esports. La aplicación incluye funcionalidades como autenticación de usuarios, gestión de equipos, torneos, resultados, recompensas, soporte y un asistente de soporte IA con AWS Bedrock.

### Tecnologías principales usadas

- Backend: Django + Django REST Framework
- Base de datos: PostgreSQL
- Cola y tareas asíncronas: Redis + Celery
- Servidor WSGI: Gunicorn
- Contenerización: Docker + Docker Compose
- Frontend: plantillas Django + CSS/JS
- Entorno de desarrollo: Visual Studio Code y Pycharm PRO (Antiguamente)

### En qué fases y para qué se han usado contenedores

Los contenedores se han usado durante todo el ciclo de desarrollo, especialmente en:

1. Desarrollo local diario:
   - Arranque de servicios con una sola orden (`docker compose up -d`).
   - Entorno homogéneo para backend, base de datos, Redis y Mailpit.

2. Pruebas y validaciones:
   - Ejecución de migraciones y comandos de Django dentro del contenedor web.
   - Verificación de logs de ejecución de servicios y errores de integración.

3. Integración de nuevas funcionalidades:
   - Pruebas de la API de soporte con Bedrock sin depender del entorno del sistema host.
   - Ajustes de configuración de variables de entorno y reinicio controlado de servicios.

4. Preparación para despliegue:
   - Construcción de imagen Docker versionada.
   - Reproducibilidad del entorno para facilitar paso a staging/producción.

---

## 2. Integración de los contenedores en el IDE

En este proyecto, la integración con contenedores en el IDE (Visual Studio Code) se ha hecho exclusivamente mediante la terminal integrada.

### Herramienta del IDE usada

- Terminal integrada de VS Code.

No se han usado extensiones específicas para gestionar contenedores desde interfaz gráfica; toda la operativa se ha realizado por línea de comandos.

### Acciones realizadas y finalidad

1. Levantar y detener el stack de servicios:
   - Finalidad: disponer del entorno completo de desarrollo.
   - Comandos típicos:
     - `docker compose up -d`
     - `docker compose down`

2. Reconstruir servicios tras cambios de código/configuración:
   - Finalidad: aplicar cambios de dependencias, código o variables de entorno.
   - Comando típico:
     - `docker compose up -d --build web`

3. Ejecutar comandos dentro del contenedor web:
   - Finalidad: mantener consistencia del entorno Python/Django.
   - Comandos típicos:
     - `docker compose exec web python manage.py migrate`
     - `docker compose exec web python manage.py check`

4. Revisar logs para depuración:
   - Finalidad: detectar errores de ejecución, configuración e integración con servicios externos.
   - Comando típico:
     - `docker compose logs web`

### Acción pormenorizada (pasos y resultado)

Acción elegida: aplicación de migraciones en entorno contenerizado.

Pasos seguidos:

1. Iniciar servicios necesarios:
   - `docker compose up -d`

2. Ejecutar migraciones desde el contenedor web:
   - `docker compose exec web python manage.py migrate`

3. Verificar salida de terminal y logs:
   - Comprobar que las migraciones se aplican sin errores.
   - Si hay incidencia, revisar con `docker compose logs web`.

4. Corregir y repetir si es necesario:
   - Ajustar código/configuración.
   - Reconstruir servicio web con `docker compose up -d --build web`.

Resultado obtenido:

- La base de datos quedó sincronizada con el estado del código.
- Se evitó el clásico problema de diferencias entre entorno local y entorno objetivo.
- Se agilizó la depuración al tener todos los servicios conectados bajo Docker Compose.

---

## 3. Conclusiones

La integración de contenedores durante el desarrollo ha aportado beneficios claros:

1. Reproducibilidad del entorno:
   - El proyecto funciona con la misma configuración en cualquier equipo.

2. Aislamiento de dependencias:
   - Se evita contaminar el sistema local con versiones concretas de paquetes o servicios.

3. Flujo de trabajo más estable:
   - Ejecutar comandos siempre dentro del contenedor reduce errores de versión y configuración.

4. Depuración más ordenada:
   - Los logs por servicio permiten detectar incidencias de forma más rápida.

Como principal inconveniente, la reconstrucción de imágenes y algunos arranques pueden consumir tiempo, especialmente tras cambios relevantes. Aun así, el balance general ha sido positivo: el uso de contenedores y su manejo desde la terminal del IDE ha mejorado la fiabilidad del desarrollo y la preparación para despliegue.
