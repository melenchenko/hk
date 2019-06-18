from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.test, name='test'),
    path('demo/', include('app.modules.demo.urls')),
]
