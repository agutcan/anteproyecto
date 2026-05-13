# 📁 Estructura del proyecto

---

```bash
📂 anteproyecto/
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
│   ├── 📄 __init__.py                # Marca el directorio como un paquete Python
│   ├── 🛠 admin.py                  # Registro de modelos en el panel admin de Django
│   ├── 🧰 apps.py                   # Configuración de la app
│   ├── 🧩 context_processors.py      # Context processors para inyectar datos globales en las plantillas
│   ├── 📝 forms.py                  # Formularios de Django
│   ├── 🧮 functions.py              # Funciones auxiliares y lógica reutilizable
│   ├── 🧱 models.py                 # Definición de modelos y estructura de datos
│   ├── 📦 serializers.py            # Serializadores para DRF (API)
│   ├── ⏱ tasks.py                  # Tareas asíncronas con Celery
│   ├── 🧭 urls.py                   # Rutas específicas de la app
│   └── 👁 views.py                  # Vistas web o API (Django/DRF)
│
├── 🤖 subirEC2/                      # Microservicio FastAPI para el soporte IA
│   ├── 📄 .env.example              # Plantilla de variables de entorno
│   ├── 🐳 docker-compose.yml        # Orquestación de contenedores del microservicio
│   ├── 🐳 Dockerfile                # Imagen Docker del microservicio
│   ├── 📘 README.md                 # Documentación específica de subirEC2
│   ├── 📦 requirements.txt         # Dependencias Python del microservicio
│   ├── 📂 app/                      # Código fuente del servicio IA
│   │   ├── 📄 __init__.py           # Marca el paquete Python del microservicio
│   │   ├── ⚙️ config.py             # Configuración general del servicio y variables de entorno
│   │   ├── 🧠 embeddings.py         # Carga y gestión de modelos de embeddings
│   │   ├── 📝 ingest.py             # Proceso de ingesta e indexado de documentos
│   │   ├── 🚀 main.py               # Punto de entrada de la API FastAPI
│   │   ├── 🔎 rag.py                # Lógica de recuperación y generación de respuestas
│   │   ├── 🧾 schemas.py            # Esquemas y modelos de datos de la API
│   │   ├── ✍️ text_utils.py         # Utilidades para limpieza y tratamiento de texto
│   │   ├── 🗄 vector_store.py       # Gestión del almacén vectorial y búsquedas semánticas
│   │   └── 📂 providers/            # Adaptadores de proveedores LLM/embeddings
│   └── 📚 documents/               # Base documental del chatbot de soporte
│       └── 📄 ...
├── 📄 .env.example                    # Plantilla de variables de entorno
├── 🚫 .gitignore                     # Archivos y carpetas ignorados por Git
├── 🐳 Dockerfile                     # Imagen Docker del proyecto
├── 📘 README.md                      # Documentación general del proyecto
├── 🐙 docker-compose.yml            # Orquestación de contenedores (Django, BD, Redis, etc.)
├── 📂 .github/workflows/              # Workflows de GitHub Actions para CI/CD y despliegue
│   ├── 🛠 docker_aws.yml             # Workflow de despliegue principal en AWS
│   └── 🤖 subirEC2-documents.yml     # Workflow para reindexar documentos y reconstruir el soporte IA
├── 🛠 manage.py                      # Comando de gestión de Django
└── 📦 requirements.txt               # Dependencias del proyecto (pip)

```

# 🗃️ Esquema de la base de datos (Generado desde pycharm)

![Esquema de la base de datos](../web/static/images/diagrama.png)

---

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