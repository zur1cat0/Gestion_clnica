from django.test import TestCase
from django.urls import reverse

from diagnostico.models import Diagnostico
from recepcion.models import Equipo

from .models import Entrega


class DespachoWorkflowTests(TestCase):
    def setUp(self):
        session = self.client.session
        session["autenticado"] = True
        session.save()
        self.equipo = Equipo.objects.create(
            nombre="Cliente despacho",
            tipo="Notebook",
            problema="No inicia",
            estado="L",
        )
        self.diagnostico = Diagnostico.objects.create(
            equipo=self.equipo,
            estudiante="Técnico inicial",
            diagnostico="Equipo reparado y listo",
            listo_para_despacho=True,
        )

    def test_dispatch_urls_use_the_new_prefix_and_legacy_prefix_still_works(self):
        self.assertEqual(reverse("listado_entregas"), "/despacho/listado/")
        self.assertEqual(reverse("verificar_entrega"), "/despacho/verificar/")
        response = self.client.get("/entrega/listado/")
        self.assertEqual(response.status_code, 200)

    def test_only_ready_equipment_can_be_registered_for_dispatch(self):
        response = self.client.get(reverse("verificar_entrega"))
        self.assertContains(response, "Cliente despacho")
        self.assertNotContains(response, 'name="monto"')

        response = self.client.post(
            reverse("verificar_entrega"),
            {
                "diagnostico_id": self.diagnostico.id,
                "observaciones": "Entregar en recepción",
            },
        )

        despacho = Entrega.objects.get(diagnostico=self.diagnostico)
        self.assertRedirects(
            response,
            reverse("comprobante_entrega", args=[despacho.id]),
        )
        self.assertEqual(despacho.observaciones, "Entregar en recepción")

    def test_non_ready_equipment_does_not_appear_in_dispatch_queue(self):
        self.equipo.estado = "H"
        self.equipo.save(update_fields=["estado"])

        response = self.client.get(reverse("verificar_entrega"))

        self.assertNotContains(response, "Cliente despacho")
        self.assertEqual(Entrega.objects.count(), 0)
