import os
import dj_database_url
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver', '[::1]']

# Use DATABASE_URL if provided (e.g. Neon PostgreSQL), else fallback to SQLite
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and not DATABASE_URL.startswith('sqlite'):
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Email settings for local development:
# Outputs emails directly to the console terminal instead of sending over SMTP.
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'webmaster@localhost')
CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL', '')

