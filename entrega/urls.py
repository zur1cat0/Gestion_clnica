from django.urls import path
from . import views

app_name = 'entrega'

urlpatterns = [
    path('verificar/', views.verificar_view, name='verificar'),
    path('reporte/', views.reporte_view, name='reporte'),
    path('comprobante/', views.comprobante_view, name='comprobante'),
]