from django.contrib import admin

from .models import IntervencionHardware


@admin.register(IntervencionHardware)
class IntervencionHardwareAdmin(admin.ModelAdmin):
    list_display = ("equipo", "tecnico", "siguiente_paso", "fecha_intervencion")
    list_filter = ("siguiente_paso", "fecha_intervencion")
    search_fields = ("equipo__nombre", "equipo__tipo", "tecnico", "diagnostico", "solucion")
