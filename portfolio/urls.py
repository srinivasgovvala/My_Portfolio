"""URL configuration for portfolio project."""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import RedirectView
from django.views.static import serve
from core.sitemaps import PortfolioSitemap
from core.views import download_resume

sitemaps = {'portfolio': PortfolioSitemap}

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.svg', permanent=True)),
    path('admin/', admin.site.urls),
    path('media/resume/resume.pdf', download_resume, name='direct_resume_media'),
    path('resume.pdf', download_resume, name='direct_resume_pdf'),
    path('', include('core.urls')),
    path('projects/', include('projects.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('contact/', include('contact.urls')),
    path('music/', include('music.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
