
```bash
my_project/
│
├── manage.py                     # Comando principal de Django para gestionar el proyecto
├── db.sqlite3                    # Base de datos SQLite (si no usas otro sistema de base de datos)
├── my_project/                   # Carpeta del proyecto principal de Django
│   ├── __init__.py
│   ├── settings.py                # Configuración principal del proyecto
│   ├── urls.py                    # Enrutamiento principal de la aplicación
│   ├── asgi.py                    # Configuración ASGI (para despliegue en servidores)
│   └── wsgi.py                    # Configuración WSGI (para despliegue en servidores)
│
├── apps/                          # Carpeta para las aplicaciones (apps) del proyecto
│   ├── tournaments/               # Aplicación para manejar los torneos
│   │   ├── __init__.py
│   │   ├── models.py              # Modelos relacionados con torneos
│   │   ├── views.py               # Vistas para la gestión de torneos
│   │   ├── serializers.py         # Serializadores para las API de tor
```

## 🔄 Navegación
[⬅️ Volver al README principal](../README.md)
