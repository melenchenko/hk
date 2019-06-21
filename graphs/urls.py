from django.urls import path
from graphs import views

urlpatterns = [
    path('', views.graph, name='graph'),
]
