# ArenaGG - Docker Image

Production-ready Docker image for the ArenaGG Django application.

## Image

- Repository: `agutcan/anteproyecto`
- Tag: `latest`
- Full name: `agutcan/anteproyecto:latest`

## What is inside

- Python 3.13 slim base image
- Django app served with Gunicorn (4 workers, 2 threads)
- System dependencies for PostgreSQL builds (psycopg2)
- Non-root runtime user (`django`)
- WhiteNoise for static files

## Quick start

Pull the image:

```bash
docker pull agutcan/anteproyecto:latest
```

Run a container:

```bash
docker run --rm -p 8000:8000 --env-file .env agutcan/anteproyecto:latest \
  gunicorn ArenaGG.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 2
```

## Required environment variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DEBUG` | Django debug mode | `True` / `False` |
| `SECRET_KEY` | Django secret key | `django-insecure-...` |
| `DATABASE_URL` | PostgreSQL connection string | `postgres://user:pass@host/db` |
| `POSTGRES_DB` | Database name | `django_db` |
| `POSTGRES_USER` | Database user | `postgres` |
| `POSTGRES_PASSWORD` | Database password | `password` |
| `POSTGRES_HOST` | Database host | `db` |
| `EMAIL_HOST` | SMTP server host | `mailpit` |
| `EMAIL_PORT` | SMTP server port | `1025` |
| `CELERY_BROKER_URL` | Redis broker for Celery | `redis://redis:6379/0` |

## Optional environment variables

| Variable | Description |
|----------|-------------|
| `SUPPORT_AI_API_URL` | Microservicio de soporte IA | `http://127.0.0.1:8081/chat` |
| `SUPPORT_AI_TIMEOUT` | Timeout para el chatbot | `20` |
| `IMAGE` | Image tag for Docker Compose | `agutcan/anteproyecto:latest` |
| `MP_MAX_MESSAGES` | Mailpit max stored messages | `5000` |
| `MP_DATABASE` | Mailpit database path | `/data/mailpit.db` |

## Volumes (optional)

For persistent static/media files:

```bash
docker run --rm -p 8000:8000 --env-file .env \
  -v $(pwd)/staticfiles:/app/staticfiles \
  -v $(pwd)/web/static/media:/app/web/static/media \
  agutcan/anteproyecto:latest \
  gunicorn ArenaGG.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 2
```

## Full stack deployment

This image is designed to run as part of a full stack. Use Docker Compose for complete deployments:

```bash
cp .env.example .env
# Edit .env with your values
docker compose up -d
docker compose exec web python manage.py migrate
```

The compose file includes: Traefik (reverse proxy + SSL), Django web, PostgreSQL, Redis, Celery, Celery Beat, Mailpit, and Nginx for media files.

## CI/CD

The image is built and pushed automatically via GitHub Actions (`docker_aws.yml`) on every push to `main`. The workflow:
1. Validates code format with **Black**
2. Builds the Docker image
3. Pushes to Docker Hub
4. Deploys to AWS EC2 via SSH

## Notes

- Never publish real credentials in environment files. Use `.env` locally and secrets in production.
- The image runs as a **non-root user** (`django`) for security.
- For production, set `DEBUG=False` and use a strong `SECRET_KEY`.
- Traefik `v2.11` is used for the reverse proxy (newer versions had SSL bugs).
