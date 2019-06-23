from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.about, name='about'),
    path('project', views.project, name='about')
]
