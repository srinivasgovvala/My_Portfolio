"""
WSGI config for portfolio project.

It exposes the WSGI callable as a module-level variable named ``application``
and ``app`` (required by Vercel serverless environment).
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ.get('DJANGO_SETTINGS_MODULE', 'portfolio.settings.production'))

application = get_wsgi_application()
app = application
