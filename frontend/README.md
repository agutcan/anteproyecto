# Frontend Angular — primeros componentes

He creado una estructura mínima con componentes base y servicios para consumir la API Django:

- `app/components/header` — `header.component` (HTML/SCSS/TS)
- `app/components/footer` — `footer.component`
- `app/components/home` — `home.component`
- `app/components/game-list` — lista de juegos que consume `/api/games/`
- `app/services/api.service.ts` — cliente HTTP con token
- `app/services/auth.service.ts` — login y manejo de tokens

Para arrancar en desarrollo (usa Angular CLI si lo tienes instalado globalmente):

```bash
# desde la raíz del repo
cd frontend
npm install
npm start
```

O puedes usar `npx -p @angular/cli@20.3.1 ng serve` si no quieres instalar globalmente.

Nota: esta estructura es intencionalmente mínima. Si quieres que genere un `ng new` completo y compile el proyecto, puedo hacerlo (tardará más y descargará dependencias). Si quieres que adapte las plantillas HTML existentes del proyecto a componentes más detallados, dime qué vistas quieres primero (por ejemplo `tournament-list`, `player-profile`).
