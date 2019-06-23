from django.urls import path
from . import views

urlpatterns = [
    path('load', views.load, name='demo-load'),
    path('view', views.view, name='demo-view'),
    path('view/<int:pk>', views.view, name='demo-view_'),
    path('analyze', views.analyze, name='demo-analyze'),
    path('analyze/<int:pk>', views.analyze, name='demo-analyze_'),
    path('settings', views.settings, name='demo-settings'),
    path('graph', views.graph, name='demo-graph'),
    path('graph/<int:pk>', views.graph, name='demo-graph_'),
    path('analyze_bigdata/<slug:type>', views.analyze_bigdata, name='bigdata'),
]
