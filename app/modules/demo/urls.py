from django.urls import path
from . import views

urlpatterns = [
    path('load', views.load, name='demo-load'),
    path('view/<int:pk>', views.view, name='demo-view'),
    path('analyze', views.analyze, name='demo-analyze'),
    path('settings', views.settings, name='demo-settings'),
]
