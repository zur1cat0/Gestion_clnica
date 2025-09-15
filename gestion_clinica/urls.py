from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", include("login.urls")),
    path("recepcion/", include("recepcion.urls")),
    path("diagnostico/", include("diagnostico.urls")),
    path("entrega/", include("entrega.urls")),
]
