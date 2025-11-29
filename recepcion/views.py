from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Equipo


def _requerir_login(request):
    if not request.session.get("autenticado"):
        return redirect("login")
    return None


def registrar_equipo(request):
    """
    Registra un equipo en la clínica (Recepción).
    """
    redirect_login = _requerir_login(request)
    if redirect_login:
        return redirect_login

    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        correo = request.POST.get("correo", "").strip()
        telefono = request.POST.get("telefono", "").strip()

        tipo = request.POST.get("tipo", "")
        tipo_otro = request.POST.get("tipo_otro", "").strip()
        problema = request.POST.get("problema", "")
        problema_otro = request.POST.get("problema_otro", "").strip()

        # Resolver "Otro" en tipo y problema
        if tipo == "Otro":
            tipo_final = tipo_otro
        else:
            tipo_final = tipo

        if problema == "Otro":
            problema_final = problema_otro
        else:
            problema_final = problema

        if not nombre or not tipo_final or not problema_final:
            messages.error(
                request,
                "Nombre del cliente, tipo de equipo y problema reportado son obligatorios.",
            )
        else:
            Equipo.objects.create(
                nombre=nombre,
                correo=correo if correo else None,
                telefono=telefono if telefono else None,
                tipo=tipo_final,
                problema=problema_final,
            )
            messages.success(request, "Equipo recepcionado correctamente.")
            return redirect("listar_equipos")

    return render(request, "recepcion/registrar.html")


def listar_equipos(request):
    """
    Lista de equipos recepcionados.
    """
    redirect_login = _requerir_login(request)
    if redirect_login:
        return redirect_login

    equipos = Equipo.objects.all().order_by("-fecha_recepcion")
    return render(request, "recepcion/listado.html", {"equipos": equipos})


def detalle_equipo(request, equipo_id):
    """
    Detalle de un equipo recepcionado (si lo estás usando).
    """
    redirect_login = _requerir_login(request)
    if redirect_login:
        return redirect_login

    equipo = get_object_or_404(Equipo, id=equipo_id)
    return render(request, "recepcion/detalles.html", {"equipo": equipo})
