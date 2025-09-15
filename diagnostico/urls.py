from django.urls import path
from . import views

app_name = 'diagnostico'

urlpatterns = [
    path('asignar/', views.asignar_view, name='asignar'),
    path('evaluar/', views.evaluar_view, name='evaluar'),
    path('listado/', views.listado_view, name='listado'),
]
