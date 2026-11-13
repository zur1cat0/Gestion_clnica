from django.db import models

from recepcion.models import Equipo


class IntervencionHardware(models.Model):
    SIGUIENTES_PASOS = [
        ("S", "Enviar a Software"),
        ("L", "Listo para despacho"),
    ]

    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        related_name="intervenciones_hardware",
        verbose_name="Equipo",
    )
    tecnico = models.CharField("Técnico", max_length=100)
    diagnostico = models.TextField("Diagnóstico de hardware")
    solucion = models.TextField("Solución de hardware")
    siguiente_paso = models.CharField(
        "Siguiente paso",
        max_length=1,
        choices=SIGUIENTES_PASOS,
    )
    fecha_intervencion = models.DateTimeField("Fecha de intervención", auto_now_add=True)

    class Meta:
        ordering = ["-fecha_intervencion", "-id"]
        verbose_name = "Intervención de hardware"
        verbose_name_plural = "Intervenciones de hardware"

    def __str__(self):
        return f"Hardware: {self.equipo} ({self.fecha_intervencion:%d/%m/%Y})"
