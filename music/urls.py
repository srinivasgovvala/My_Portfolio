from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    path('tracks/', views.track_list, name='tracks'),
]
