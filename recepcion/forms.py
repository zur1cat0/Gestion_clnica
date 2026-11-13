from django import forms
from .models import Equipo


class EquipoForm(forms.ModelForm):
    """
    Formulario basado en el modelo Equipo.
    Se utiliza para validar y gestionar los datos
    al registrar y editar equipos en Recepción.
    """

    class Meta:
        model = Equipo
        fields = [
            "nombre",
            "correo",
            "telefono",
            "tipo",
            "problema",
            "preguntas_cliente",
        ]
