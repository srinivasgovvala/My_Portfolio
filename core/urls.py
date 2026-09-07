from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('health/', views.health_check, name='health_check'),
    path('robots.txt', views.robots_txt, name='robots'),
    path('resume/', views.download_resume, name='resume'),
    path('download-resume/', views.download_resume, name='download_resume'),
]
