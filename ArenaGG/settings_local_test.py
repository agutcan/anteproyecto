from .settings import *
from pathlib import Path

# Archivo de settings temporal para pruebas locales: usa SQLite
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Permitir todas las ORIGINS en pruebas locales
CORS_ALLOW_ALL_ORIGINS = True
