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
    /entrega/ → siempre lleva al listado de entregas.
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
    ).order_by("-fecha_entrega")

    return render(request, "entrega/listado.html", {"entregas": entregas})


def verificar_entrega(request):
    """
    Pantalla para GENERAR una nueva entrega usando TU template verificar.html.

    - GET: muestra diagnósticos sin entrega + formulario de monto/observaciones.
    - POST: crea la Entrega y redirige al comprobante.
    """
    redirect_login = _requerir_login(request)
    if redirect_login:
        return redirect_login

    # Diagnósticos que aún NO tienen entrega asociada
    diagnosticos_pendientes = Diagnostico.objects.filter(
        entrega__isnull=True
    ).select_related("equipo")

    if request.method == "POST":
        diag_id = request.POST.get("diagnostico_id", "").strip()
        monto_str = request.POST.get("monto", "").strip()
        observaciones = request.POST.get("observaciones", "").strip()

        if not diag_id or not monto_str:
            messages.error(
                request,
                "Debes seleccionar un diagnóstico y escribir el monto.",
            )
        else:
            try:
                monto = float(monto_str)
            except ValueError:
                messages.error(request, "El monto debe ser un número válido.")
            else:
                diagnostico = get_object_or_404(Diagnostico, id=diag_id)

                # Evitamos duplicar entregas para el mismo diagnóstico
                if hasattr(diagnostico, "entrega"):
                    messages.warning(
                        request,
                        "Ese diagnóstico ya tiene una entrega registrada.",
                    )
                else:
                    entrega = Entrega.objects.create(
                        diagnostico=diagnostico,
                        monto=monto,
                        observaciones=observaciones,
                        entregado=False,
                    )
                    messages.success(request, "Entrega registrada correctamente.")
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
        Entrega.objects.select_related("diagnostico__equipo"), id=entrega_id
    )
    entrega.entregado = True
    entrega.save()

    equipo = entrega.diagnostico.equipo
    # Si tu modelo Equipo tiene estados, aquí lo marcamos como 'Entregado'
    try:
        equipo.estado = "E"
        equipo.save()
    except Exception:
        # Si no tiene campo estado, simplemente lo ignoramos
        pass

    messages.success(
        request,
        f"La entrega para {equipo.nombre} ha sido marcada como COMPLETADA.",
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
    ).order_by("-fecha_entrega")

    return render(request, "entrega/reporte.html", {"entregas": entregas})
