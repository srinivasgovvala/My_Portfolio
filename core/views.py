import os
import sys
import json
import traceback
from pathlib import Path
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.db import connection
from .models import HeroRole
from profile_app.models import Skill, Technology
from education.models import Education
from experience.models import Experience
from projects.models import Project, FutureProject
from contact.forms import ContactForm


def home(request):
    hero_roles = HeroRole.objects.filter(is_active=True).order_by('order')
    skills = Skill.objects.filter(is_active=True).order_by('category', 'order')
    technologies = Technology.objects.filter(is_active=True).order_by('category', 'order')
    educations = Education.objects.filter(is_active=True).order_by('order', '-id')
    experiences = Experience.objects.filter(is_active=True).order_by('order', '-start_date')
    featured_projects = Project.objects.filter(is_featured=True, is_completed=True).order_by('order')
    future_projects = FutureProject.objects.filter(is_active=True).order_by('order')
    contact_form = ContactForm()

    context = {
        'hero_roles': hero_roles,
        'skills': skills,
        'technologies': technologies,
        'educations': educations,
        'experiences': experiences,
        'featured_projects': featured_projects,
        'future_projects': future_projects,
        'contact_form': contact_form,
    }
    return render(request, 'core/home.html', context)


def health_check(request):
    """Diagnostic health check endpoint for debugging Vercel deployment."""
    report = {
        'status': 'healthy',
        'python_version': sys.version,
        'django_settings_module': os.environ.get('DJANGO_SETTINGS_MODULE', 'not set'),
        'has_database_url_env': bool(os.environ.get('DATABASE_URL')),
        'database_engine': connection.settings_dict.get('ENGINE', 'unknown'),
        'database_host': connection.settings_dict.get('HOST', 'unknown'),
        'base_dir': str(settings.BASE_DIR),
        'template_dirs': [str(d) for d in settings.TEMPLATES[0].get('DIRS', [])],
    }

    # Inspect filesystem for templates
    found_templates = []
    for search_root in [settings.BASE_DIR, Path('/var/task')]:
        if search_root.exists():
            for p in search_root.rglob('*.html'):
                if '.venv' not in str(p) and '__pycache__' not in str(p):
                    found_templates.append(str(p))
    report['found_html_files'] = found_templates

    # Test Database Query
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            report['db_ping'] = 'SUCCESS'
    except Exception as e:
        report['status'] = 'error'
        report['db_ping_error'] = str(e)
        report['traceback'] = traceback.format_exc()

    # Test Model Fetch
    try:
        report['hero_roles_count'] = HeroRole.objects.count()
        report['projects_count'] = Project.objects.count()
        report['skills_count'] = Skill.objects.count()
    except Exception as e:
        report['status'] = 'error'
        report['model_query_error'] = str(e)
        if 'traceback' not in report:
            report['traceback'] = traceback.format_exc()

    return JsonResponse(report, json_dumps_params={'indent': 2})


def robots_txt(request):
    content = """User-agent: *
Allow: /
Disallow: /admin/
Sitemap: {scheme}://{host}/sitemap.xml
""".format(scheme=request.scheme, host=request.get_host())
    return HttpResponse(content, content_type='text/plain')
