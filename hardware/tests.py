from django.test import TestCase
from django.urls import reverse

from recepcion.models import Equipo

from .models import IntervencionHardware


class HardwareWorkflowTests(TestCase):
    def setUp(self):
        session = self.client.session
        session["autenticado"] = True
        session.save()
        self.equipo = Equipo.objects.create(
            nombre="Cliente hardware",
            tipo="Notebook",
            problema="No enciende",
            estado="H",
        )

    def test_hardware_can_route_to_software_and_preserves_its_work(self):
        response = self.client.post(
            reverse("hardware_home"),
            {
                "equipo": self.equipo.id,
                "tecnico": "Técnico Hardware",
                "diagnostico": "Memoria RAM defectuosa",
                "solucion": "Se reemplazó el módulo RAM",
                "siguiente_paso": "S",
            },
        )

        self.assertRedirects(response, reverse("hardware_home"))
        self.equipo.refresh_from_db()
        self.assertEqual(self.equipo.estado, "S")
        self.assertEqual(
            IntervencionHardware.objects.get().solucion,
            "Se reemplazó el módulo RAM",
        )

    def test_hardware_can_mark_equipment_ready_for_dispatch(self):
        response = self.client.post(
            reverse("hardware_home"),
            {
                "equipo": self.equipo.id,
                "tecnico": "Técnico Hardware",
                "diagnostico": "Conector de energía suelto",
                "solucion": "Se aseguró el conector",
                "siguiente_paso": "L",
            },
        )

        self.assertRedirects(response, reverse("hardware_home"))
        self.equipo.refresh_from_db()
        self.assertEqual(self.equipo.estado, "L")

    def test_hardware_cannot_process_an_equipment_in_another_stage(self):
        self.equipo.estado = "S"
        self.equipo.save(update_fields=["estado"])

        response = self.client.post(
            reverse("hardware_home"),
            {
                "equipo": self.equipo.id,
                "tecnico": "Técnico Hardware",
                "diagnostico": "Diagnóstico",
                "solucion": "Solución",
                "siguiente_paso": "L",
            },
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(IntervencionHardware.objects.count(), 0)
