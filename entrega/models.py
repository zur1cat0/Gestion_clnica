from django.db import models
from diagnostico.models import Diagnostico


class Entrega(models.Model):
    diagnostico = models.OneToOneField(
        Diagnostico,
        on_delete=models.CASCADE,
        related_name="entrega",
        verbose_name="Diagnóstico asociado",
    )
    monto = models.DecimalField(
        "Monto a cobrar",
        max_digits=10,
        decimal_places=2,
        default=0,  # evita dramas
    )
    entregado = models.BooleanField("¿Entregado al cliente?", default=False)
    observaciones = models.TextField("Observaciones al entregar", blank=True)
    fecha_entrega = models.DateTimeField("Fecha de entrega", auto_now_add=True)

    def __str__(self):
        return f"Entrega {self.diagnostico.equipo.nombre} (${self.monto})"
