from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Equipo
from .forms import EquipoForm


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

    # Formulario vacío por defecto (para solicitudes GET)
    form = EquipoForm()

    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        correo = request.POST.get("correo", "").strip()
        telefono = request.POST.get("telefono", "").strip()

        tipo = request.POST.get("tipo", "")
        tipo_otro = request.POST.get("tipo_otro", "").strip()
        problema = request.POST.get("problema", "")
        problema_otro = request.POST.get("problema_otro", "").strip()

        # Resolver "Otro" en tipo y problema (igual que antes)
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
            # Usamos EquipoForm para validar y guardar
            data = {
                "nombre": nombre,
                "correo": correo if correo else None,
                "telefono": telefono if telefono else None,
                "tipo": tipo_final,
                "problema": problema_final,
            }
            form = EquipoForm(data=data)
            if form.is_valid():
                form.save()
                messages.success(request, "Equipo recepcionado correctamente.")
                return redirect("listar_equipos")
            else:
                messages.error(
                    request,
                    "Hay errores en el formulario. Por favor revisa los datos ingresados.",
                )

    # Para GET o si hubo errores, renderizamos el formulario
    return render(request, "recepcion/registrar.html", {"form": form})


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

    ⚠ No permite editar si el equipo ya fue ENTREGADO (estado = 'E').
    """
    redirect_login = _requerir_login(request)
    if redirect_login:
        return redirect_login

    equipo = get_object_or_404(Equipo, id=equipo_id)

    # ⛔ Bloquear edición si el equipo ya fue entregado
    if equipo.estado == "E":
        messages.error(
            request,
            "No se puede editar un equipo ya entregado.",
        )
        return redirect("listar_equipos")

    # Form inicial con los datos actuales (para GET)
    form = EquipoForm(instance=equipo)

    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        correo = request.POST.get("correo", "").strip()
        telefono = request.POST.get("telefono", "").strip()

        tipo = request.POST.get("tipo", "")
        tipo_otro = request.POST.get("tipo_otro", "").strip()
        problema = request.POST.get("problema", "")
        problema_otro = request.POST.get("problema_otro", "").strip()

        # Resolver "Otro" en tipo y problema (igual que antes)
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
            # Usamos EquipoForm con instancia para actualizar
            data = {
                "nombre": nombre,
                "correo": correo if correo else None,
                "telefono": telefono if telefono else None,
                "tipo": tipo_final,
                "problema": problema_final,
            }
            form = EquipoForm(data=data, instance=equipo)
            if form.is_valid():
                form.save()
                messages.success(request, "Equipo actualizado correctamente.")
                return redirect("listar_equipos")
            else:
                messages.error(
                    request,
                    "Hay errores en el formulario. Por favor revisa los datos ingresados.",
                )

    return render(request, "recepcion/registrar.html", {"equipo": equipo, "form": form})


def eliminar_equipo(request, equipo_id):
    """
    Elimina un equipo recepcionado (Delete del CRUD).
    Muestra una página de confirmación y, si se confirma, elimina el registro.

    ⚠ No permite eliminar si el equipo ya fue ENTREGADO (estado = 'E').
    """
    redirect_login = _requerir_login(request)
    if redirect_login:
        return redirect_login

    equipo = get_object_or_404(Equipo, id=equipo_id)

    # ⛔ Bloquear eliminación si el equipo ya fue entregado
    if equipo.estado == "E":
        messages.error(
            request,
            "No se puede eliminar un equipo ya entregado.",
        )
        return redirect("listar_equipos")

    if request.method == "POST":
        nombre_equipo = f"{equipo.nombre} – {equipo.tipo}"
        equipo.delete()
        messages.success(request, f"Equipo '{nombre_equipo}' eliminado correctamente.")
        return redirect("listar_equipos")

    # Si es GET, mostramos la página de confirmación
    return render(request, "recepcion/eliminar.html", {"equipo": equipo})
