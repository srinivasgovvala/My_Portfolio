from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from projects.models import Project


class PortfolioSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        pages = ['core:home']
        project_slugs = Project.objects.filter(is_completed=True).values_list('slug', flat=True)
        return pages + [f'project:{slug}' for slug in project_slugs]

    def location(self, item):
        if item == 'core:home':
            return reverse('core:home')
        slug = item.replace('project:', '')
        return reverse('projects:detail', kwargs={'slug': slug})
