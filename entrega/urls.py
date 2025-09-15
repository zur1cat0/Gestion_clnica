from django.urls import path
from . import views

urlpatterns = [
    path("verificar/", views.verificar, name="verificar_entrega"),
    path("reporte/", views.reporte, name="reporte_entrega"),
    path("comprobante/", views.comprobante, name="comprobante_entrega"),
]
