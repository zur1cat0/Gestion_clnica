from django.test import TestCase
from django.urls import reverse

from recepcion.models import Equipo

from .models import IntervencionSoftware


class SoftwareWorkflowTests(TestCase):
    def setUp(self):
        session = self.client.session
        session["autenticado"] = True
        session.save()
        self.equipo = Equipo.objects.create(
            nombre="Cliente software",
            tipo="PC de escritorio",
            problema="No inicia el sistema",
            estado="S",
        )

    def test_software_can_route_back_to_hardware(self):
        response = self.client.post(
            reverse("software_home"),
            {
                "equipo": self.equipo.id,
                "tecnico": "Técnico Software",
                "diagnostico": "Controlador incompatible",
                "solucion": "Se reinstaló el controlador",
                "siguiente_paso": "H",
            },
        )

        self.assertRedirects(response, reverse("software_home"))
        self.equipo.refresh_from_db()
        self.assertEqual(self.equipo.estado, "H")
        self.assertEqual(
            IntervencionSoftware.objects.get().diagnostico,
            "Controlador incompatible",
        )

    def test_software_can_mark_equipment_ready_for_dispatch(self):
        response = self.client.post(
            reverse("software_home"),
            {
                "equipo": self.equipo.id,
                "tecnico": "Técnico Software",
                "diagnostico": "Archivos de inicio dañados",
                "solucion": "Se reparó el inicio",
                "siguiente_paso": "L",
            },
        )

        self.assertRedirects(response, reverse("software_home"))
        self.equipo.refresh_from_db()
        self.assertEqual(self.equipo.estado, "L")
