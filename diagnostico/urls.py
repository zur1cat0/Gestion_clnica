from django.urls import path
from . import views

urlpatterns = [
    # /diagnostico/  → redirige al listado
    path("", views.diagnostico_home, name="diagnostico_home"),

    # /diagnostico/asignar/
    path("asignar/", views.asignar_equipo, name="asignar_equipo"),

    # /diagnostico/evaluar/
    path("evaluar/", views.evaluar_equipo, name="evaluar_equipo"),

    # /diagnostico/listado/
    path("listado/", views.listado_diagnosticos, name="listado_diagnosticos"),
]
