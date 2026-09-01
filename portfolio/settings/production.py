import os
import dj_database_url
from .base import *

# Default DEBUG to False for production, allow override via env var
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes')

# Host configuration: Allow all hosts in production on Vercel
ALLOWED_HOSTS = ['*']

# CSRF Trusted Origins for Vercel & custom domains
CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',
    'https://*.now.sh',
    'http://localhost',
    'http://127.0.0.1',
]

vercel_url = os.environ.get('VERCEL_URL')
if vercel_url:
    CSRF_TRUSTED_ORIGINS.append(f'https://{vercel_url}')

env_csrf = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
if env_csrf:
    CSRF_TRUSTED_ORIGINS.extend([origin.strip() for origin in env_csrf.split(',') if origin.strip()])

# Database configuration: support DATABASE_URL (Neon PostgreSQL) with fallback to verified Neon DB
DEFAULT_NEON_DB_URL = 'postgresql://user:password@localhost:5432/dbname'
DATABASE_URL = os.environ.get('DATABASE_URL', DEFAULT_NEON_DB_URL)

DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=0,  # 0 for serverless Lambdas (Vercel) to avoid connection leaks
        conn_health_checks=False,
        ssl_require=True
    )
}

# Reverse proxy SSL header
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static files handling with WhiteNoise
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
WHITENOISE_MANIFEST_STRICT = False

# Email settings
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() in ('true', '1', 'yes')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'srinivasgovvala12@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER or 'srinivasgovvala12@gmail.com')
CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL', 'srinivasgovvala12@gmail.com')
