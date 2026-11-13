from django.db import models


class Equipo(models.Model):
    TIPOS_EQUIPO = [
        ("PC de escritorio", "PC de escritorio"),
        ("Notebook", "Notebook"),
    ]

    ESTADOS = [
        ("R", "Recepcionado"),
        ("D", "En diagnóstico"),
        ("H", "Pendiente en Hardware"),
        ("S", "Pendiente en Software"),
        ("L", "Listo para despacho"),
        ("E", "Despachado"),
    ]

    # Datos del cliente
    nombre = models.CharField("Nombre del cliente", max_length=100)
    correo = models.EmailField(
        "Correo del cliente", max_length=254, blank=True, null=True
    )
    telefono = models.CharField(
        "Teléfono del cliente", max_length=20, blank=True, null=True
    )

    # Datos del equipo
    tipo = models.CharField(
        "Tipo de equipo",
        max_length=100,
        choices=TIPOS_EQUIPO,
    )
    problema = models.TextField("Problema reportado")
    preguntas_cliente = models.TextField(
        "Información del equipo",
        blank=True,
    )

    fecha_recepcion = models.DateTimeField("Fecha de recepción", auto_now_add=True)
    estado = models.CharField("Estado", max_length=1, choices=ESTADOS, default="R")

    def __str__(self):
        return f"{self.nombre} – {self.tipo}"
