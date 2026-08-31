from django.shortcuts import render, get_object_or_404
from .models import Project, FutureProject


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, is_completed=True)
    related = Project.objects.filter(is_completed=True).exclude(pk=project.pk).order_by('order')[:3]
    return render(request, 'projects/detail.html', {
        'project': project,
        'related_projects': related,
    })


def future_project(request, slug):
    project = get_object_or_404(FutureProject, slug=slug, is_active=True)
    return render(request, 'projects/future_detail.html', {'project': project})
