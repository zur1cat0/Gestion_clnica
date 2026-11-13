from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from recepcion.models import Equipo

from .forms import IntervencionSoftwareForm


def _requerir_login(request):
    if not request.session.get("autenticado"):
        return redirect("login")
    return None


def software_home(request):
    redirect_login = _requerir_login(request)
    if redirect_login:
        return redirect_login

    equipos = (
        Equipo.objects.filter(estado="S")
        .prefetch_related("intervenciones_software")
        .order_by("fecha_recepcion", "id")
    )
    if request.method == "POST":
        equipo = get_object_or_404(Equipo, pk=request.POST.get("equipo"), estado="S")
        form = IntervencionSoftwareForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                intervencion = form.save(commit=False)
                intervencion.equipo = equipo
                intervencion.save()
                equipo.estado = form.cleaned_data["siguiente_paso"]
                equipo.save(update_fields=["estado"])

            if equipo.estado == "H":
                messages.success(
                    request,
                    f"Intervención registrada. {equipo.nombre} pasó a Hardware.",
                )
            else:
                messages.success(
                    request,
                    f"Intervención registrada. {equipo.nombre} quedó listo para despacho.",
                )
            return redirect("software_home")
        messages.error(request, "Revisa los datos de la intervención.")
        return render(
            request,
            "software/listado.html",
            {"equipos": equipos, "form": form, "equipo_error_id": equipo.id},
        )

    return render(request, "software/listado.html", {"equipos": equipos})
