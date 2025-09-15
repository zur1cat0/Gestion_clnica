from django.urls import path
from . import views

urlpatterns = [
    path("asignar/", views.asignar, name="asignar_equipo"),
    path("evaluar/", views.evaluar, name="evaluar_equipo"),
    path("listado/", views.listado, name="listado_diagnosticos"),
]
