from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Equipo
from .forms import EquipoForm


PROBLEMAS_PREDEFINIDOS = [
    "No enciende",
    "Pantalla rota",
    "Batería dañada",
    "Sobrecalentamiento",
    "Daño por agua",
]


def _formulario_equipo(request, instance=None):
    data = request.POST.copy() if request.method == "POST" else None
    if data and data.get("problema") == "Otro":
        data["problema"] = data.get("problema_otro", "").strip()
    return EquipoForm(data=data, instance=instance)


def _requerir_login(request):
    if not request.session.get("autenticado"):
        return redirect("login")
    return None


def registrar_equipo(request):
    """
    Registra un equipo en la clínica (Recepción).
    Usa EquipoForm (ModelForm) para validar los datos.
    """
    redirect_login = _requerir_login(request)
    if redirect_login:
        return redirect_login

    form = _formulario_equipo(request)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Equipo recepcionado correctamente.")
            return redirect("listar_equipos")
        messages.error(
            request,
            "Hay errores en el formulario. Por favor revisa los datos ingresados.",
        )

    # Para GET o si hubo errores, renderizamos el formulario
    return render(
        request,
        "recepcion/registrar.html",
        {"form": form, "problemas_predefinidos": PROBLEMAS_PREDEFINIDOS},
    )


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
    Detalle de un equipo recepcionado.
    """
    redirect_login = _requerir_login(request)
    if redirect_login:
        return redirect_login

    equipo = get_object_or_404(Equipo, id=equipo_id)
    return render(request, "recepcion/detalles.html", {"equipo": equipo})


def editar_equipo(request, equipo_id):
    """
    Edita los datos de un equipo recepcionado (Update del CRUD).
    Usa EquipoForm (ModelForm) para validar los datos.

    No permite editar si el equipo ya fue despachado.
    """
    redirect_login = _requerir_login(request)
    if redirect_login:
        return redirect_login

    equipo = get_object_or_404(Equipo, id=equipo_id)

    # Bloquear edición si el equipo ya fue despachado.
    if equipo.estado == "E":
        messages.error(
            request,
            "No se puede editar un equipo ya despachado.",
        )
        return redirect("listar_equipos")

    form = _formulario_equipo(request, instance=equipo)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Equipo actualizado correctamente.")
            return redirect("listar_equipos")
        messages.error(
            request,
            "Hay errores en el formulario. Por favor revisa los datos ingresados.",
        )

    return render(
        request,
        "recepcion/registrar.html",
        {
            "equipo": equipo,
            "form": form,
            "problemas_predefinidos": PROBLEMAS_PREDEFINIDOS,
        },
    )


def eliminar_equipo(request, equipo_id):
    """
    Elimina un equipo recepcionado (Delete del CRUD).
    Muestra una página de confirmación y, si se confirma, elimina el registro.

    No permite eliminar si el equipo ya fue despachado.
    """
    redirect_login = _requerir_login(request)
    if redirect_login:
        return redirect_login

    equipo = get_object_or_404(Equipo, id=equipo_id)

    # Bloquear eliminación si el equipo ya fue despachado.
    if equipo.estado == "E":
        messages.error(
            request,
            "No se puede eliminar un equipo ya despachado.",
        )
        return redirect("listar_equipos")

    if request.method == "POST":
        nombre_equipo = f"{equipo.nombre} – {equipo.tipo}"
        equipo.delete()
        messages.success(request, f"Equipo '{nombre_equipo}' eliminado correctamente.")
        return redirect("listar_equipos")

    # Si es GET, mostramos la página de confirmación
    return render(request, "recepcion/eliminar.html", {"equipo": equipo})
