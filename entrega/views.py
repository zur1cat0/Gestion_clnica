from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Entrega
from diagnostico.models import Diagnostico


def _requerir_login(request):
    if not request.session.get("autenticado"):
        return redirect("login")
    return None


def entrega_home(request):
    """
    /despacho/ → listado principal de despachos.
    """
    redirect_login = _requerir_login(request)
    if redirect_login:
        return redirect_login
    return redirect("listado_entregas")


def listado_entregas(request):
    """
    Tabla con todas las entregas registradas.
    """
    redirect_login = _requerir_login(request)
    if redirect_login:
        return redirect_login

    entregas = Entrega.objects.select_related(
        "diagnostico",
        "diagnostico__equipo",
    ).prefetch_related(
        "diagnostico__equipo__intervenciones_hardware",
        "diagnostico__equipo__intervenciones_software",
    ).order_by("-fecha_entrega")

    return render(request, "entrega/listado.html", {"entregas": entregas})


def verificar_entrega(request):
    """
    Pantalla para GENERAR una nueva entrega usando TU template verificar.html.

    - GET: muestra diagnósticos sin despacho y el formulario de observaciones.
    - POST: crea la Entrega y redirige al comprobante.
    """
    redirect_login = _requerir_login(request)
    if redirect_login:
        return redirect_login

    # Diagnósticos que aún NO tienen entrega asociada
    diagnosticos_pendientes = (
        Diagnostico.objects.filter(
            equipo__estado="L",
            entrega__isnull=True,
        )
        .select_related("equipo")
        .prefetch_related(
            "equipo__intervenciones_hardware",
            "equipo__intervenciones_software",
        )
    )

    if request.method == "POST":
        diag_id = request.POST.get("diagnostico_id", "").strip()
        observaciones = request.POST.get("observaciones", "").strip()

        if not diag_id:
            messages.error(request, "Debes seleccionar un equipo listo para despacho.")
        else:
            diagnostico = get_object_or_404(
                Diagnostico,
                id=diag_id,
                equipo__estado="L",
            )

            # Evitamos duplicar entregas para el mismo diagnóstico
            if hasattr(diagnostico, "entrega"):
                messages.warning(
                    request,
                    "Ese diagnóstico ya tiene un despacho registrado.",
                )
            else:
                entrega = Entrega.objects.create(
                    diagnostico=diagnostico,
                    observaciones=observaciones,
                    entregado=False,
                )
                messages.success(request, "Despacho registrado correctamente.")
                return redirect("comprobante_entrega", entrega_id=entrega.id)

    context = {
        "diagnosticos_pendientes": diagnosticos_pendientes,
    }
    return render(request, "entrega/verificar.html", context)


def comprobante_entrega(request, entrega_id):
    """
    Muestra el comprobante de entrega usando tu template comprobante_de_entrega.html.
    """
    redirect_login = _requerir_login(request)
    if redirect_login:
        return redirect_login

    entrega = get_object_or_404(
        Entrega.objects.select_related(
            "diagnostico",
            "diagnostico__equipo",
        ).prefetch_related(
            "diagnostico__equipo__intervenciones_hardware",
            "diagnostico__equipo__intervenciones_software",
        ),
        id=entrega_id,
    )

    context = {
        "entrega": entrega,
        "diagnostico": entrega.diagnostico,
        "equipo": entrega.diagnostico.equipo,
    }
    return render(request, "entrega/comprobante_de_entrega.html", context)


def confirmar_entrega(request, entrega_id):
    """
    Marca la entrega como ENTREGADA y cambia el estado del equipo.
    """
    redirect_login = _requerir_login(request)
    if redirect_login:
        return redirect_login

    entrega = get_object_or_404(
        Entrega.objects.select_related("diagnostico__equipo").prefetch_related(
            "diagnostico__equipo__intervenciones_hardware",
            "diagnostico__equipo__intervenciones_software",
        ),
        id=entrega_id,
    )
    entrega.entregado = True
    entrega.save()

    equipo = entrega.diagnostico.equipo
    # Si tu modelo Equipo tiene estados, aquí lo marcamos como 'Entregado'
    equipo.estado = "E"
    equipo.save(update_fields=["estado"])

    messages.success(
        request,
        f"El despacho para {equipo.nombre} ha sido marcado como COMPLETADO.",
    )
    return redirect("listado_entregas")


def reporte_entregas(request):
    """
    Reporte general usando tu template entrega/reporte.html.
    """
    redirect_login = _requerir_login(request)
    if redirect_login:
        return redirect_login

    entregas = Entrega.objects.select_related(
        "diagnostico",
        "diagnostico__equipo",
    ).prefetch_related(
        "diagnostico__equipo__intervenciones_hardware",
        "diagnostico__equipo__intervenciones_software",
    ).order_by("-fecha_entrega")

    return render(request, "entrega/reporte.html", {"entregas": entregas})


# ------------------ CRUD extra de Entrega: Editar / Eliminar ------------------ #
def editar_entrega(request, entrega_id):
    """
    Edita las observaciones del despacho.
    No permite editar si la entrega ya está marcada como entregada.
    """
    redirect_login = _requerir_login(request)
    if redirect_login:
        return redirect_login

    entrega = get_object_or_404(
        Entrega.objects.select_related("diagnostico__equipo"),
        id=entrega_id,
    )

    # Bloqueo de negocio: no editar si ya está entregada
    if entrega.entregado:
        messages.error(
            request,
            "No se puede editar una entrega ya marcada como entregada.",
        )
        return redirect("listado_entregas")

    if request.method == "POST":
        observaciones = request.POST.get("observaciones", "").strip()
        entrega.observaciones = observaciones
        entrega.save(update_fields=["observaciones"])
        messages.success(request, "Despacho actualizado correctamente.")
        return redirect("listado_entregas")

    context = {
        "entrega": entrega,
        "diagnostico": entrega.diagnostico,
        "equipo": entrega.diagnostico.equipo,
    }
    return render(request, "entrega/entrega_form.html", context)


def eliminar_entrega(request, entrega_id):
    """
    Elimina una entrega.
    No permite eliminar si la entrega ya está marcada como entregada.
    """
    redirect_login = _requerir_login(request)
    if redirect_login:
        return redirect_login

    entrega = get_object_or_404(
        Entrega.objects.select_related("diagnostico__equipo"),
        id=entrega_id,
    )

    # Bloqueo de negocio: no eliminar si ya está entregada
    if entrega.entregado:
        messages.error(
            request,
            "No se puede eliminar una entrega ya marcada como entregada.",
        )
        return redirect("listado_entregas")

    if request.method == "POST":
        entrega.delete()
        messages.success(request, "Despacho eliminado correctamente.")
        return redirect("listado_entregas")

    context = {
        "entrega": entrega,
        "diagnostico": entrega.diagnostico,
        "equipo": entrega.diagnostico.equipo,
    }
    return render(request, "entrega/entrega_eliminar.html", context)
