from django.db import models
from diagnostico.models import Diagnostico


class Entrega(models.Model):
    diagnostico = models.OneToOneField(
        Diagnostico,
        on_delete=models.CASCADE,
        related_name="entrega",
        verbose_name="Diagnóstico asociado",
    )
    entregado = models.BooleanField("¿Despachado al cliente?", default=False)
    observaciones = models.TextField("Observaciones de despacho", blank=True)
    fecha_entrega = models.DateTimeField("Fecha de despacho", auto_now_add=True)

    class Meta:
        verbose_name = "Despacho"
        verbose_name_plural = "Despachos"

    def __str__(self):
        return f"Despacho {self.diagnostico.equipo.nombre}"
