from django.urls import path
from . import views, demo

urlpatterns = [
    path('', views.test, name='test'),
    path('demo/load', demo.load, name='demo-load'),
    path('demo/view', demo.view, name='demo-view'),
    path('demo/analyze', demo.analyze, name='demo-analyze'),
    path('demo/settings', demo.settings, name='demo-settings'),
]
