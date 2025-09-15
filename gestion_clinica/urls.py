from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('login.urls', namespace='login')),
    path('recepcion/', include('recepcion.urls', namespace='recepcion')),
    path('diagnostico/', include('diagnostico.urls', namespace='diagnostico')),
    path('entrega/', include('entrega.urls', namespace='entrega')),
    path('', RedirectView.as_view(url='/login/', permanent=False)),
]