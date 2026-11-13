from django.urls import path

from . import views


urlpatterns = [
    path("", views.hardware_home, name="hardware_home"),
]
