from django.shortcuts import render
from django.http import HttpResponse
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


def robots_txt(request):
    content = """User-agent: *
Allow: /
Disallow: /admin/
Sitemap: {scheme}://{host}/sitemap.xml
""".format(scheme=request.scheme, host=request.get_host())
    return HttpResponse(content, content_type='text/plain')
