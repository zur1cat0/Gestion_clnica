from django.db import models
from recepcion.models import Equipo


class Estudiante(models.Model):
    nombre = models.CharField("Nombre", max_length=100)
    correo = models.EmailField("Correo", blank=True, null=True)
    telefono = models.CharField(
        "Teléfono",
        max_length=20,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    nombre = models.CharField("Nombre del servicio", max_length=100)
    descripcion = models.TextField("Descripción", blank=True)
    precio = models.PositiveIntegerField("Precio", default=0)

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

    def __str__(self):
        return self.nombre


class Asignacion(models.Model):
    """
    Relación persistente entre Equipo y Estudiante (técnico).
    Un equipo solo debe tener una asignación activa a la vez.
    """
    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        related_name="asignaciones",
        verbose_name="Equipo",
    )
    estudiante = models.ForeignKey(
        Estudiante,
        on_delete=models.CASCADE,
        related_name="asignaciones",
        verbose_name="Estudiante / Técnico",
    )
    fecha_asignacion = models.DateTimeField("Fecha de asignación", auto_now_add=True)
    activo = models.BooleanField("Asignación activa", default=True)

    class Meta:
        verbose_name = "Asignación de equipo"
        verbose_name_plural = "Asignaciones de equipos"

    def __str__(self):
        return f"{self.estudiante} → {self.equipo}"


class Diagnostico(models.Model):
    AREAS_SOPORTE = [
        ("hardware", "Hardware"),
        ("software", "Software"),
    ]

    ESTADOS = [
        ("E", "En diagnóstico"),
        ("F", "Finalizado"),
    ]

    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        related_name="diagnosticos",
        verbose_name="Equipo recepcionado",
    )
    # Se guarda el nombre del técnico en texto, para mantener historial
    estudiante = models.CharField("Estudiante / Técnico", max_length=100)
    diagnostico = models.TextField("Diagnóstico")
    # Kept for historical diagnoses; new solutions are recorded in Hardware or Software.
    solucion = models.TextField(
        "Solución aplicada (histórica)",
        blank=True,
        default="",
        editable=False,
    )
    tipo_solucion = models.CharField(
        "Tipo de solución (histórico)",
        max_length=20,
        blank=True,
        null=True,
        editable=False,
    )
    siguiente_area = models.CharField(
        "Área siguiente",
        max_length=10,
        choices=AREAS_SOPORTE,
        blank=True,
    )
    listo_para_despacho = models.BooleanField(
        "Listo para despacho sin pasar por Hardware o Software",
        default=False,
    )
    estado = models.CharField(
        "Estado del diagnóstico",
        max_length=1,
        choices=ESTADOS,
        default="F",
    )
    fecha_diagnostico = models.DateTimeField(
        "Fecha diagnóstico",
        auto_now_add=True,
    )

    def __str__(self):
        return f"Diag de {self.equipo} por {self.estudiante}"
