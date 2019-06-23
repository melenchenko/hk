from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main, name='page-main'),
    path('demo/', include('app.modules.demo.urls')),
    path('opros/<int:pk>', views.opros, name='opros_'),
    path('opros', views.opros, name='opros-main'),
]
