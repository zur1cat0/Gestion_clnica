from django.urls import path
from . import views

urlpatterns = [
    path("registrar/", views.registrar_equipo, name="registrar_equipo"),
    path("listado/", views.listar_equipos, name="listar_equipos"),
    path("detalle/<int:equipo_id>/", views.detalle_equipo, name="detalle_equipo"),
    path("editar/<int:equipo_id>/", views.editar_equipo, name="editar_equipo"),
    path("eliminar/<int:equipo_id>/", views.eliminar_equipo, name="eliminar_equipo"),
]
