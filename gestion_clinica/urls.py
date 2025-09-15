from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_login(request):
    return redirect('/login/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_login),
    path('login/', include('login.urls')),
    path('recepcion/', include('recepcion.urls')),
    path('diagnostico/', include('diagnostico.urls')),
    path('entrega/', include('entrega.urls')),
]