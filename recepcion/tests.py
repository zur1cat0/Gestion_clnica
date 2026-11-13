from django.test import TestCase
from django.urls import reverse

from diagnostico.models import Asignacion, Diagnostico, Estudiante
from entrega.models import Entrega
from hardware.models import IntervencionHardware
from software.models import IntervencionSoftware

from .forms import EquipoForm
from .models import Equipo


class RecepcionEquipoTests(TestCase):
    def setUp(self):
        session = self.client.session
        session["autenticado"] = True
        session.save()

    def test_registration_saves_client_questions_and_rejects_other_devices(self):
        response = self.client.get(reverse("registrar_equipo"))
        self.assertContains(response, "Información del equipo")
        self.assertNotContains(response, "Preguntas realizadas al cliente")

        response = self.client.post(
            reverse("registrar_equipo"),
            {
                "nombre": "Cliente de prueba",
                "correo": "",
                "telefono": "",
                "tipo": "Notebook",
                "problema": "Otro",
                "problema_otro": "Se apaga al usarlo",
                "preguntas_cliente": "¿Cuándo comenzó?\nAyer.",
            },
        )

        self.assertRedirects(response, reverse("listar_equipos"))
        equipo = Equipo.objects.get()
        self.assertEqual(equipo.tipo, "Notebook")
        self.assertEqual(equipo.problema, "Se apaga al usarlo")
        self.assertEqual(equipo.preguntas_cliente, "¿Cuándo comenzó?\nAyer.")

        response = self.client.post(
            reverse("registrar_equipo"),
            {
                "nombre": "Otro cliente",
                "tipo": "Celular",
                "problema": "No enciende",
                "preguntas_cliente": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Select a valid choice.", status_code=200)
        self.assertEqual(Equipo.objects.count(), 1)

    def test_questions_and_device_type_are_visible_through_diagnosis_and_delivery(self):
        equipo = Equipo.objects.create(
            nombre="Cliente seguimiento",
            tipo="PC de escritorio",
            problema="No enciende",
            preguntas_cliente="¿Se escuchan sonidos?\nNo.",
        )
        estudiante = Estudiante.objects.create(nombre="Técnico de prueba")

        response = self.client.get(reverse("listar_equipos"))
        self.assertContains(response, "PC de escritorio")
        self.assertContains(response, "¿Se escuchan sonidos?")

        response = self.client.get(
            reverse("detalle_equipo", args=[equipo.id])
        )
        self.assertContains(response, "Información del equipo")
        self.assertContains(response, "¿Se escuchan sonidos?")

        response = self.client.get(
            reverse("editar_equipo", args=[equipo.id])
        )
        self.assertContains(response, "¿Se escuchan sonidos?")

        response = self.client.get(reverse("asignar_equipo"))
        self.assertContains(response, "PC de escritorio")
        self.assertContains(response, "¿Se escuchan sonidos?")

        response = self.client.post(
            reverse("asignar_equipo"),
            {"equipo": equipo.id, "estudiante": estudiante.id},
        )
        self.assertRedirects(response, reverse("evaluar_equipo"))

        response = self.client.get(reverse("evaluar_equipo"))
        self.assertContains(response, "PC de escritorio")
        self.assertContains(response, "¿Se escuchan sonidos?")

        response = self.client.post(
            reverse("evaluar_equipo"),
            {
                "idx": "0",
                "diagnostico": "Fuente de poder defectuosa",
                "siguiente_area": "hardware",
            },
        )
        self.assertRedirects(response, reverse("listado_diagnosticos"))

        response = self.client.get(reverse("listado_diagnosticos"))
        self.assertContains(response, "PC de escritorio")
        self.assertContains(response, "¿Se escuchan sonidos?")
        self.assertContains(response, "Pendiente en Hardware")

        diagnostico = Diagnostico.objects.get(equipo=equipo)
        response = self.client.get(reverse("historial_diagnosticos"))
        self.assertContains(response, "¿Se escuchan sonidos?")

        response = self.client.get(
            reverse("editar_diagnostico", args=[diagnostico.id])
        )
        self.assertContains(response, "¿Se escuchan sonidos?")

        response = self.client.get(
            reverse("eliminar_diagnostico", args=[diagnostico.id])
        )
        self.assertContains(response, "¿Se escuchan sonidos?")

        response = self.client.get(reverse("verificar_entrega"))
        self.assertNotContains(response, "Cliente seguimiento")

        response = self.client.get(reverse("hardware_home"))
        self.assertContains(response, "¿Se escuchan sonidos?")
        response = self.client.post(
            reverse("hardware_home"),
            {
                "equipo": equipo.id,
                "tecnico": "Técnico de Hardware",
                "diagnostico": "Conector de energía dañado",
                "solucion": "Se revisó el conector de energía",
                "siguiente_paso": "S",
            },
        )
        self.assertRedirects(response, reverse("hardware_home"))

        response = self.client.get(reverse("software_home"))
        self.assertContains(response, "Cliente seguimiento")
        response = self.client.post(
            reverse("software_home"),
            {
                "equipo": equipo.id,
                "tecnico": "Técnico de Software",
                "diagnostico": "Sistema operativo dañado",
                "solucion": "Se reparó el inicio del sistema",
                "siguiente_paso": "H",
            },
        )
        self.assertRedirects(response, reverse("software_home"))

        response = self.client.get(reverse("hardware_home"))
        self.assertContains(response, "Cliente seguimiento")
        response = self.client.post(
            reverse("hardware_home"),
            {
                "equipo": equipo.id,
                "tecnico": "Técnico de Hardware",
                "diagnostico": "Conector de energía dañado",
                "solucion": "Se reemplazó el conector",
                "siguiente_paso": "L",
            },
        )
        self.assertRedirects(response, reverse("hardware_home"))

        response = self.client.get(reverse("listado_diagnosticos"))
        self.assertContains(response, "Se reemplazó el conector")
        response = self.client.get(reverse("verificar_entrega"))
        self.assertContains(response, "¿Se escuchan sonidos?")
        self.assertContains(response, "Cliente seguimiento")

        entrega = Entrega.objects.create(diagnostico=diagnostico)

        response = self.client.get(
            reverse("comprobante_entrega", args=[entrega.id])
        )
        self.assertContains(response, "Información del equipo")
        self.assertNotContains(response, "Monto total del despacho")
        self.assertContains(response, "PC de escritorio")
        self.assertContains(response, "¿Se escuchan sonidos?")
        self.assertContains(response, "Se reemplazó el conector")
        self.assertContains(response, "Se reparó el inicio del sistema")
        self.assertEqual(IntervencionHardware.objects.filter(equipo=equipo).count(), 2)
        self.assertEqual(IntervencionSoftware.objects.filter(equipo=equipo).count(), 1)

        response = self.client.get(reverse("listado_entregas"))
        self.assertContains(response, "¿Se escuchan sonidos?")

        response = self.client.get(reverse("reporte_entregas"))
        self.assertContains(response, "¿Se escuchan sonidos?")

        response = self.client.get(reverse("editar_entrega", args=[entrega.id]))
        self.assertContains(response, "¿Se escuchan sonidos?")

        response = self.client.get(
            reverse("eliminar_entrega", args=[entrega.id])
        )
        self.assertContains(response, "¿Se escuchan sonidos?")

    def test_device_form_has_only_the_two_supported_types(self):
        self.assertEqual(
            tuple(
                value
                for value, _ in EquipoForm().fields["tipo"].choices
                if value
            ),
            ("PC de escritorio", "Notebook"),
        )
