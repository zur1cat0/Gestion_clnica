from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


def home(request):
    """
    Página raíz:
    - Si el usuario está autenticado en la sesión, va directo a recepción.
    - Si no, va al login.
    """
    if request.session.get('autenticado'):
        return redirect('registrar_equipo')
    return redirect('login')


urlpatterns = [
    path('', home, name='home'),
    path('login/', include('login.urls')),
    path('recepcion/', include('recepcion.urls')),
    path('diagnostico/', include('diagnostico.urls')),
    path('entrega/', include('entrega.urls')),
    path('admin/', admin.site.urls),
]
