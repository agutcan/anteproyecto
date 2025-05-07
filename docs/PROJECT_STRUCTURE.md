# Estructura del proyecto

---

```bash
anteproyecto/
│
├── ArenaGG/                           # Carpeta del proyecto Django principal
│   ├── __init__.py                    # Marca el directorio como un paquete Python
│   ├── settings.py                    # Configuración global del proyecto (BD, apps, middleware, etc.)
│   ├── urls.py                        # Enrutamiento de URLs a nivel global del proyecto
│   ├── asgi.py                        # Punto de entrada ASGI para servidores asincrónicos (ej. Daphne, Uvicorn)
│   ├── celery.py                      # Configuración de Celery para tareas asíncronas
│   └── wsgi.py                        # Punto de entrada WSGI para servidores web (ej. Gunicorn, uWSGI)
│
├── data/                              # Carpeta opcional para guardar datos locales en mi caso usado para guardar los datos de mailpit.
│   ├── ...                            # Puede contener archivos como `initial_data.json`, `seeds.py`, etc.
│
├── docs/                              # Documentación del proyecto (guías, especificaciones, diagramas)
│   ├── ...                            # Archivos Markdown, PDF o imágenes relacionadas con la documentación
│
├── templates/                         # Plantillas globales compartidas por varias apps en mi caso para el registro/login (HTML base, etc.)
│   ├── ...                            # Archivos HTML y otros templates reutilizables
│
├── web/                               # Aplicación Django principal que contiene la lógica del dominio
│   ├── migrations/                    # Migraciones de base de datos de esta app
│   ├── ...
│   ├── static/                        # Archivos estáticos propios de la app (CSS, JS, imágenes)
│   ├── ...
│   ├── templates/                     # Plantillas HTML específicas de la app
│   ├── ...
│   ├── tests/                         # Tests unitarios y de integración para la app
│   ├── ...                   
│   ├── admin.py                       # Registro de modelos en el admin de Django
│   ├── apps.py                        # Configuración de la app para Django
│   ├── forms.py                       # Formularios de Django utilizados en vistas o admin
│   ├── functions.py                   # Funciones auxiliares (lógica de negocio reutilizable)
│   ├── models.py                      # Definición de modelos y estructura de la base de datos
│   ├── serializers.py                 # Serializadores (para APIs REST con Django REST Framework)
│   ├── tasks.py                       # Tareas asíncronas ejecutadas con Celery
│   ├── urls.py                        # Rutas específicas de esta app
│   ├── views.py                       # Vistas web (Django) y/o vistas API (DRF)
│
├── .gitignore                         # Lista de archivos/carpetas que Git debe ignorar
├── Dockerfile                         # Instrucciones para crear una imagen Docker del proyecto
├── README.md                          # Descripción del proyecto, instrucciones de instalación y uso
├── docker-compose.yml                 # Despliegue de contenedores (Django, BD, Redis, etc.)
├── manage.py                          # Script para gestionar tareas del proyecto (ej. runserver, migrate)
└── requirements.txt                   # Lista de dependencias del proyecto (para `pip install`)
```

## 🔄 Navegación
[⬅️ Volver al README principal](../README.md)
