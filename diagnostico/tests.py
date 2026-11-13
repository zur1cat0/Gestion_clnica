from django.test import TestCase
from django.urls import reverse

from recepcion.models import Equipo

from .models import Asignacion, Diagnostico, Estudiante


class DiagnosticoWorkflowTests(TestCase):
    def setUp(self):
        session = self.client.session
        session["autenticado"] = True
        session.save()
        self.equipo = Equipo.objects.create(
            nombre="Cliente diagnóstico",
            tipo="Notebook",
            problema="Se apaga",
            estado="D",
        )
        self.estudiante = Estudiante.objects.create(nombre="Técnico inicial")
        self.asignacion = Asignacion.objects.create(
            equipo=self.equipo,
            estudiante=self.estudiante,
            activo=True,
        )
        self.client.session["asignacion_reciente_id"] = self.asignacion.id
        self.client.session.save()

    def test_initial_diagnosis_routes_to_hardware_without_a_solution(self):
        self.client.get(reverse("evaluar_equipo"))
        response = self.client.post(
            reverse("evaluar_equipo"),
            {
                "idx": "0",
                "diagnostico": "Posible falla en la memoria",
                "siguiente_area": "hardware",
            },
        )

        self.assertRedirects(response, reverse("listado_diagnosticos"))
        diagnostico = Diagnostico.objects.get(equipo=self.equipo)
        self.assertEqual(diagnostico.diagnostico, "Posible falla en la memoria")
        self.assertEqual(diagnostico.solucion, "")
        self.assertFalse(diagnostico.tipo_solucion)
        self.assertEqual(diagnostico.siguiente_area, "hardware")
        self.equipo.refresh_from_db()
        self.assertEqual(self.equipo.estado, "H")
        self.asignacion.refresh_from_db()
        self.assertFalse(self.asignacion.activo)

    def test_bypass_marks_equipment_ready_for_dispatch(self):
        self.client.get(reverse("evaluar_equipo"))
        response = self.client.post(
            reverse("evaluar_equipo"),
            {
                "idx": "0",
                "diagnostico": "Equipo operativo, sin reparación necesaria",
                "listo_para_despacho": "on",
            },
        )

        self.assertRedirects(response, reverse("listado_diagnosticos"))
        diagnostico = Diagnostico.objects.get(equipo=self.equipo)
        self.assertTrue(diagnostico.listo_para_despacho)
        self.assertEqual(diagnostico.siguiente_area, "")
        self.equipo.refresh_from_db()
        self.assertEqual(self.equipo.estado, "L")

    def test_initial_diagnosis_requires_an_area_or_dispatch_bypass(self):
        self.client.get(reverse("evaluar_equipo"))
        response = self.client.post(
            reverse("evaluar_equipo"),
            {
                "idx": "0",
                "diagnostico": "Requiere revisión adicional",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Diagnostico.objects.count(), 0)
        self.equipo.refresh_from_db()
        self.assertEqual(self.equipo.estado, "D")
