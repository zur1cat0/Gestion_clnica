from django.contrib import admin
from .models import Equipo


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "estado", "fecha_recepcion")
    search_fields = ("nombre", "tipo", "problema", "preguntas_cliente")
    list_filter = ("estado", "tipo")
