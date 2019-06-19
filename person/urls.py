from django.urls import path, include
from person import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/success/', TemplateView.as_view(template_name="registration/success.html"),
             name='register-success'),
    path('register/', views.Register.as_view(), name='register'),
]
