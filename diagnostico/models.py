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
    # Aquí se guarda algo como "[Preventiva] Cambio de pantalla (Servicios: ...)"
    solucion = models.TextField("Solución aplicada")
    # Campo explícito para el tipo de solución (Preventiva / Correctiva)
    tipo_solucion = models.CharField(
        "Tipo de solución",
        max_length=20,
        blank=True,
        null=True,
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

    @property
    def tipo_solucion_desde_texto(self):
        """
        Si por alguna razón el campo tipo_solucion no viene,
        intenta extraer 'Preventiva' o 'Correctiva' desde self.solucion
        cuando viene así: "[Preventiva] resto..."
        """
        if self.tipo_solucion:
            return self.tipo_solucion

        if not self.solucion:
            return ""

        texto = self.solucion.strip()
        if not texto.startswith("["):
            return ""

        cierre = texto.find("]")
        if cierre <= 1:
            return ""

        return texto[1:cierre].strip()

    @property
    def solucion_detalle(self):
        """
        Devuelve la solución SIN el prefijo entre corchetes.
        Ej: "[Preventiva] Cambio de pantalla" -> "Cambio de pantalla"
        """
        if not self.solucion:
            return ""

        texto = self.solucion.strip()
        if not texto.startswith("["):
            return texto

        cierre = texto.find("]")
        if cierre == -1:
            return texto

        return texto[cierre + 1 :].strip()

    def __str__(self):
        return f"Diag de {self.equipo} por {self.estudiante}"
