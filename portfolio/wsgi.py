"""
WSGI config for portfolio project.

It exposes the WSGI callable as a module-level variable named ``application``
and ``app`` (required by Vercel serverless environment).
"""
import os
import sys
import traceback
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ.get('DJANGO_SETTINGS_MODULE', 'portfolio.settings.production'))

try:
    application = get_wsgi_application()
except Exception as e:
    sys.stderr.write(f"WSGI initialization error: {e}\n")
    traceback.print_exc(file=sys.stderr)
    raise

def app(environ, start_response):
    try:
        return application(environ, start_response)
    except Exception as e:
        sys.stderr.write(f"Request execution error: {e}\n")
        traceback.print_exc(file=sys.stderr)
        raise

