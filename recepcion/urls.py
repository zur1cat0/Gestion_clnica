from django.urls import path
from . import views

app_name = 'recepcion'

urlpatterns = [
    path('registrar/', views.registrar_view, name='registrar'),
    path('listado/', views.listado_view, name='listado'),
    path('detalle/<str:nombre>/', views.detalle_view, name='detalle'),
]