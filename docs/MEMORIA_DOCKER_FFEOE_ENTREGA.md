# Memoria de entrega: producto Docker (FFEOE / Proyecto Integrado)

## 1. Producto empaquetado en Docker

Producto: ArenaGG (plataforma web de torneos).

Archivos de referencia:

- Dockerfile: `Dockerfile`
- Compose principal historico de despliegue **(El que se usara en producción)**: `docker-composeAntiguo.yml`
- Imagen Docker Hub: `agutcan/anteproyecto:latest`

## 2. Evidencia solicitada (enlaces internos)

### 2.1 Dockerfile con comentarios

El archivo `Dockerfile` del proyecto contiene comentarios explicativos en cada etapa del build y ejecucion.

### 2.2 Imagen en Docker Hub

- Repositorio/imagen documentada: [agutcan/anteproyecto:latest](https://hub.docker.com/repository/docker/agutcan/anteproyecto/general)
- Instrucciones de uso, variables de entorno y persistencia: ver [docs/README_DOCKER_IMAGE_DOCKERHUB.md](https://github.com/agutcan/anteproyecto/blob/sinFrontend2/docs/README_DOCKER_IMAGE_DOCKERHUB.md)

### 2.3 Compose para uso de la imagen

- Archivo usado para esta memoria (Quizas se haya modificado el nombre del archivo cuando estes viendo esto): [docker-composeAntiguo.yml](https://github.com/agutcan/anteproyecto/blob/sinFrontend2/docker-composeAntiguo.yml)
- Funcionamiento y comandos: ver [docs/README_DOCKER_COMPOSE_ANTIGUO.md](https://github.com/agutcan/anteproyecto/blob/sinFrontend2/docs/README_DOCKER_COMPOSE.md)

## 3. Resumen de uso real durante el desarrollo

Durante el desarrollo del proyecto, los contenedores se han utilizado para:

- ejecucion de servicios dependientes (PostgreSQL, Redis, Mailpit),
- ejecucion de aplicacion Django con Gunicorn,
- aplicacion de migraciones y tareas de mantenimiento,
- depuracion por logs de servicio,
- reproduccion consistente del entorno en diferentes maquinas.

## 4. Notas de privacidad y seguridad

Para preservar seguridad:

- no se incluyen claves reales en documentacion de ejemplo,
- las variables sensibles deben mantenerse en `.env` local/no publico,
- los valores de ejemplo se ofrecen con placeholders cuando aplica.
