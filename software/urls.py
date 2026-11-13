from django.urls import path

from . import views


urlpatterns = [
    path("", views.software_home, name="software_home"),
]
