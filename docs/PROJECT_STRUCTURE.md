# 📁 Estructura del proyecto

---

```bash
anteproyecto/
│
├── 🧠 ArenaGG/                        # Carpeta del proyecto Django principal
│   ├── 📄 __init__.py                # Marca el directorio como un paquete Python
│   ├── ⚙️ settings.py               # Configuración global del proyecto (BD, apps, middleware, etc.)
│   ├── 🌐 urls.py                   # Enrutamiento de URLs a nivel global del proyecto
│   ├── 🚀 asgi.py                   # Punto de entrada ASGI para servidores asincrónicos (ej. Daphne, Uvicorn)
│   ├── 🐇 celery.py                 # Configuración de Celery para tareas asíncronas
│   └── 🔌 wsgi.py                   # Punto de entrada WSGI para servidores web (ej. Gunicorn, uWSGI)
│
├── 📦 data/                          # Datos locales (usado en este caso para Mailpit)
│   └── 📂 ...                        # Ej: `initial_data.json`, `seeds.py`, etc.
│
├── 📚 docs/                          # Documentación del proyecto (guías, diagramas, etc.)
│   └── 📄 ...
│
├── 🎨 templates/                     # Plantillas globales compartidas (login, base HTML, etc.)
│   └── 📄 ...
│
├── 🧩 web/                           # App principal: lógica de negocio, vistas, modelos, etc.
│   ├── 🗃 migrations/               # Migraciones de base de datos de esta app
│   │   └── 📄 ...
│   ├── 🌈 static/                   # Archivos estáticos (CSS, JS, imágenes)
│   │   └── 📄 ...
│   ├── 🖼 templates/                # Plantillas específicas de la app
│   │   └── 📄 ...
│   ├── 🧪 tests/                    # Pruebas unitarias y de integración
│   │   └── 📄 ...
│   ├── 🛠 admin.py                  # Registro de modelos en el panel admin de Django
│   ├── 🧰 apps.py                   # Configuración de la app
│   ├── 📝 forms.py                  # Formularios de Django
│   ├── 🧮 functions.py              # Funciones auxiliares y lógica reutilizable
│   ├── 🧱 models.py                 # Definición de modelos y estructura de datos
│   ├── 📦 serializers.py            # Serializadores para DRF (API)
│   ├── ⏱ tasks.py                  # Tareas asíncronas con Celery
│   ├── 🧭 urls.py                   # Rutas específicas de la app
│   └── 👁 views.py                  # Vistas web o API (Django/DRF)
│
├── 🚫 .gitignore                     # Archivos y carpetas ignorados por Git
├── 🐳 Dockerfile                     # Imagen Docker del proyecto
├── 📘 README.md                      # Documentación general del proyecto
├── 🐙 docker-compose.yml            # Orquestación de contenedores (Django, BD, Redis, etc.)
├── 🛠 manage.py                      # Comando de gestión de Django
└── 📦 requirements.txt               # Dependencias del proyecto (pip)

```

## 🔄 Navegación
[⬅️ Volver al README principal](../README.md)
