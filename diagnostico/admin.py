from django.contrib import admin
from .models import Diagnostico, Estudiante, Servicio, Asignacion


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "correo", "telefono")
    search_fields = ("nombre", "correo", "telefono")


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio")
    search_fields = ("nombre",)
    list_filter = ("precio",)


@admin.register(Asignacion)
class AsignacionAdmin(admin.ModelAdmin):
    list_display = ("equipo", "estudiante", "activo", "fecha_asignacion")
    list_filter = ("activo", "fecha_asignacion")
    search_fields = ("equipo__cliente", "equipo__tipo", "estudiante__nombre")


@admin.register(Diagnostico)
class DiagnosticoAdmin(admin.ModelAdmin):
    list_display = (
        "equipo",
        "estudiante",
        "diagnostico",
        "siguiente_area",
        "listo_para_despacho",
        "fecha_diagnostico",
    )
    search_fields = (
        "equipo__nombre",
        "equipo__tipo",
        "estudiante",
        "diagnostico",
    )
    list_filter = ("siguiente_area", "listo_para_despacho", "fecha_diagnostico")
