# Frontend (Angular) — Development and scaffolding

This project will run the Angular frontend in a separate container during development and compile to `staticfiles` for production.

Recommended local scaffold (run from project root):

```bash
# Install the specific Angular CLI globally (optional)
npm install -g @angular/cli@20.3.1

# Create an Angular app in ./frontend
npx -p @angular/cli@20.3.1 ng new frontend --routing=true --style=scss --skip-git

# Move into frontend and adjust start script if needed
cd frontend
# Ensure package.json has a start script like:
# "start": "ng serve"

# Run dev server locally (or use docker-compose)
npm start -- --host 0.0.0.0
```

Docker Compose dev (provided): the `frontend` service in `docker-compose.yml` will run `npm install && npm start`.

Production build:

```bash
cd frontend
npm run build -- --configuration production
# Copy the `dist/frontend` output into Django `staticfiles` (e.g. ./staticfiles)
```

Integration notes:
- APIs will be exposed by Django; CORS is configured for `http://localhost:4200` in `ArenaGG/settings.py`.
- Keep existing Django models; create DRF serializers and viewsets to expose API endpoints (I can scaffold these next).
