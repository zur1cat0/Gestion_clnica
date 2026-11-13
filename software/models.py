from django.db import models

from recepcion.models import Equipo


class IntervencionSoftware(models.Model):
    SIGUIENTES_PASOS = [
        ("H", "Enviar a Hardware"),
        ("L", "Listo para despacho"),
    ]

    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        related_name="intervenciones_software",
        verbose_name="Equipo",
    )
    tecnico = models.CharField("Técnico", max_length=100)
    diagnostico = models.TextField("Diagnóstico de software")
    solucion = models.TextField("Solución de software")
    siguiente_paso = models.CharField(
        "Siguiente paso",
        max_length=1,
        choices=SIGUIENTES_PASOS,
    )
    fecha_intervencion = models.DateTimeField("Fecha de intervención", auto_now_add=True)

    class Meta:
        ordering = ["-fecha_intervencion", "-id"]
        verbose_name = "Intervención de software"
        verbose_name_plural = "Intervenciones de software"

    def __str__(self):
        return f"Software: {self.equipo} ({self.fecha_intervencion:%d/%m/%Y})"
