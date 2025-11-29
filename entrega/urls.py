from django.urls import path
from . import views

urlpatterns = [
    # /entrega/  → listado principal
    path("", views.entrega_home, name="entrega_home"),

    # /entrega/listado/
    path("listado/", views.listado_entregas, name="listado_entregas"),

    # /entrega/verificar/
    # Aquí se selecciona el diagnóstico pendiente + monto y se CREA la entrega
    path("verificar/", views.verificar_entrega, name="verificar_entrega"),

    # /entrega/comprobante/<id>/
    path(
        "comprobante/<int:entrega_id>/",
        views.comprobante_entrega,
        name="comprobante_entrega",
    ),

    # /entrega/confirmar/<id>/
    path(
        "confirmar/<int:entrega_id>/",
        views.confirmar_entrega,
        name="confirmar_entrega",
    ),

    # /entrega/reporte/
    path("reporte/", views.reporte_entregas, name="reporte_entregas"),
]
