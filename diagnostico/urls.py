from django.urls import path
from . import views

urlpatterns = [
    # /diagnostico/  → redirige al listado por equipo
    path("", views.diagnostico_home, name="diagnostico_home"),

    # Flujo actual: asignar y evaluar
    path("asignar/", views.asignar_equipo, name="asignar_equipo"),
    path("evaluar/", views.evaluar_equipo, name="evaluar_equipo"),

    # Listado por equipo (ya existente)
    path("listado/", views.listado_diagnosticos, name="listado_diagnosticos"),

    # CRUD de Diagnóstico (como tal)
    path("diagnosticos/", views.historial_diagnosticos, name="historial_diagnosticos"),
    path(
        "diagnosticos/<int:diagnostico_id>/editar/",
        views.editar_diagnostico,
        name="editar_diagnostico",
    ),
    path(
        "diagnosticos/<int:diagnostico_id>/eliminar/",
        views.eliminar_diagnostico,
        name="eliminar_diagnostico",
    ),
]
