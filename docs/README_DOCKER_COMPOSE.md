# Documentacion de docker-composeAntiguo.yml

## 1. Objetivo

El archivo `docker-composeAntiguo.yml` define una arquitectura completa para ArenaGG con proxy inverso, aplicacion web, base de datos, cola de tareas, correo de pruebas y servicio de media.

## 2. Servicios definidos

1. `traefik`
- Proxy inverso y terminacion TLS.
- Gestiona dominios y certificados Let's Encrypt.

2. `whoami`
- Servicio de prueba para validar routing de Traefik.

3. `web`
- Aplicacion Django servida por Gunicorn.
- Usa la imagen `IMAGE` definida en `.env`.

4. `db`
- PostgreSQL 16 con volumen persistente.

5. `mailpit`
- SMTP de pruebas + interfaz web para revisar correos.

6. `redis`
- Broker para Celery.

7. `celery`
- Worker de tareas asicronas.

8. `celery-beat`
- Planificador de tareas periodicas.

9. `media-server`
- Nginx para servir archivos en `/media`.

## 3. Variables de entorno requeridas

Definidas via `.env`:

- `IMAGE`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `SECRET_KEY`
- `DATABASE_URL`
- `EMAIL_HOST`
- `EMAIL_PORT`
- `CELERY_BROKER_URL`

## 4. Comandos de uso

### 4.1 Arranque del stack

```bash
docker compose -f docker-composeAntiguo.yml up -d
```

### 4.2 Ver logs

```bash
docker compose -f docker-composeAntiguo.yml logs -f web
docker compose -f docker-composeAntiguo.yml logs -f traefik
```

### 4.3 Ejecutar migraciones

```bash
docker compose -f docker-composeAntiguo.yml exec web python manage.py migrate
```

### 4.4 Detener servicios

```bash
docker compose -f docker-composeAntiguo.yml down
```

### 4.5 Detener y eliminar volumenes

```bash
docker compose -f docker-composeAntiguo.yml down -v
```

## 5. Persistencia

- Base de datos: volumen `postgres_data`
- Certificados: carpeta local `./letsencrypt`
- Correo Mailpit: carpeta local `./data`
- Estaticos y media:
  - `./staticfiles:/app/staticfiles`
  - `./web/static/media:/app/web/static/media`

## 6. Seguridad y despliegue

- Se recomienda no usar credenciales de ejemplo en produccion.
- Las reglas de Traefik con dominio deben adaptarse al dominio real.
- Para produccion, usar credenciales seguras y politicas IAM de minimo privilegio.

## 7. Finalidad durante el desarrollo

Este compose se ha usado para:

- levantar todos los servicios con una orden,
- aislar dependencias del host,
- probar migraciones y tareas,
- depurar errores por servicio mediante logs,
- validar integracion web + db + redis + mail.
