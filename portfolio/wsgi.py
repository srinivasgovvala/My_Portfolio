"""
WSGI config for portfolio project.

It exposes the WSGI callable as a module-level variable named ``app`` and ``application``
(required by Vercel serverless environment).
"""
import os
import sys
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings.production')

wsgi_app = None
init_error = None

try:
    from django.core.wsgi import get_wsgi_application
    wsgi_app = get_wsgi_application()
except Exception as e:
    init_error = traceback.format_exc()

def app(environ, start_response):
    global wsgi_app, init_error
    if init_error:
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain; charset=utf-8')])
        return [f"WSGI Startup Error:\n\n{init_error}".encode('utf-8')]
    try:
        return wsgi_app(environ, start_response)
    except Exception as e:
        req_err = traceback.format_exc()
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain; charset=utf-8')])
        return [f"WSGI Request Error:\n\n{req_err}".encode('utf-8')]

application = app
