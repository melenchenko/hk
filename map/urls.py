from django.urls import path
from map import views

urlpatterns = [
    path('', views.city_map, name='map'),
]
