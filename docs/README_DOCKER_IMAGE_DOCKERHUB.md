# ArenaGG - Docker Image

Production-ready Docker image for the ArenaGG Django application.

## Image

- Repository: `agutcan/anteproyecto`
- Tag: `latest`
- Full name: `agutcan/anteproyecto:latest`

## What is inside

- Python 3.13 slim base image
- Django app served with Gunicorn
- System dependencies for PostgreSQL builds
- Non-root runtime user

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

- `DEBUG`
- `SECRET_KEY`
- `DATABASE_URL`
- `EMAIL_HOST`
- `EMAIL_PORT`
- `CELERY_BROKER_URL`

If AI support is enabled (AWS Bedrock), also configure:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `BEDROCK_KB_ID`
- `BEDROCK_MODEL_ID`
- `BEDROCK_MODEL_CANDIDATES` (optional)

## Volumes (optional)

For persistent static/media files:

```bash
docker run --rm -p 8000:8000 --env-file .env \
  -v $(pwd)/staticfiles:/app/staticfiles \
  -v $(pwd)/web/static/media:/app/web/static/media \
  agutcan/anteproyecto:latest \
  gunicorn ArenaGG.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 2
```

## Notes

- This image is designed to run as part of a full stack with PostgreSQL and Redis.
- Use Docker Compose for complete local or server deployments.
- Never publish real credentials in environment files.
