import os

# Default to production settings for Vercel deployment, allow override via DJANGO_SETTINGS_MODULE or DJANGO_ENV
env = os.environ.get('DJANGO_ENV', 'production')
if env == 'development':
    from .development import *
else:
    from .production import *
