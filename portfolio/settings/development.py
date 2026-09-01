import os
import dj_database_url
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver', '[::1]', '.vercel.app']

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

# Email settings for local testing (loads from .env)
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() in ('true', '1', 'yes')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
_raw_pwd = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_HOST_PASSWORD = _raw_pwd.replace(' ', '') if _raw_pwd else ''
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER or 'noreply@nagasrinivas.dev')
CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL', EMAIL_HOST_USER or '')
RESEND_API_KEY = os.environ.get('RESEND_API_KEY', '')
