from django.contrib import admin
from .models import Entrega


@admin.register(Entrega)
class EntregaAdmin(admin.ModelAdmin):
    list_display = (
        "diagnostico",
        "monto",
        "entregado",
        "fecha_entrega",
    )
    search_fields = ("diagnostico__equipo__nombre",)
    list_filter = ("entregado", "fecha_entrega")
