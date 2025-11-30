from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction

from recepcion.models import Equipo
from .models import Diagnostico, Estudiante, Servicio, Asignacion


# ------------------ Helper de sesión ------------------ #
def _requerir_login(request):
    if not request.session.get("autenticado"):
        return redirect("login")
    return None


# ------------------ HOME ------------------ #
def diagnostico_home(request):
    """
    Al entrar a /diagnostico/ se muestra directamente el listado.
    """
    redir = _requerir_login(request)
    if redir:
        return redir
    return redirect("listado_diagnosticos")


# ------------------ ASIGNAR EQUIPO ------------------ #
def asignar_equipo(request):
    """
    Asignar un equipo recepcionado a un estudiante (técnico).

    - Solo se pueden asignar equipos en estado 'R' (Recepcionado).
    - Se crea (o reemplaza) una Asignacion activa.
    - El equipo pasa a estado 'D' (En diagnóstico).
    - Se guarda en sesión la asignación creada para pre-seleccionarla en Evaluar.
    """
    redir = _requerir_login(request)
    if redir:
        return redir

    # Equipos que aún NO han sido asignados (R = recepcionado)
    equipos = Equipo.objects.filter(estado="R").order_by("fecha_recepcion", "id")

    # Estudiantes registrados en el admin
    estudiantes = Estudiante.objects.all().order_by("nombre")

    if request.method == "POST":
        equipo_id = request.POST.get("equipo")
        estudiante_id = request.POST.get("estudiante")

        if not equipo_id or not estudiante_id:
            messages.error(request, "Debes seleccionar un estudiante y un equipo.")
        else:
            equipo = get_object_or_404(Equipo, id=equipo_id)
            estudiante = get_object_or_404(Estudiante, id=estudiante_id)

            with transaction.atomic():
                # Desactivar asignaciones anteriores de ese equipo
                Asignacion.objects.filter(equipo=equipo, activo=True).update(
                    activo=False
                )

                # Crear nueva asignación activa
                asignacion = Asignacion.objects.create(
                    equipo=equipo,
                    estudiante=estudiante,
                    activo=True,
                )

                # Cambiar estado del equipo a "En diagnóstico"
                equipo.estado = "D"
                equipo.save()

            # Guardamos el id de la asignación para preseleccionarla en Evaluar
            request.session["asignacion_reciente_id"] = asignacion.id

            messages.success(
                request,
                f"Equipo de {equipo.nombre} asignado a {estudiante.nombre}.",
            )
            return redirect("evaluar_equipo")

    context = {
        "equipos": equipos,
        "estudiantes": estudiantes,
    }
    return render(request, "diagnostico/asignar.html", context)


# ------------------ EVALUAR EQUIPO ------------------ #
def evaluar_equipo(request):
    """
    Registrar el diagnóstico de un equipo.

    - Se muestran las asignaciones ACTIVAS (Asignacion.activo=True).
    - Se ignoran asignaciones que no tengan estudiante (datos viejos/rotos).
    - El estudiante se toma desde la Asignacion (modelo Estudiante).
    - Se guarda un Diagnostico con el nombre del estudiante en texto.
    - El equipo pasa a estado 'L' (Listo para entrega) y la asignación se marca inactiva.
    """
    redir = _requerir_login(request)
    if redir:
        return redir

    # Asignaciones activas (independiente del estado del equipo)
    asignaciones_qs = (
        Asignacion.objects.filter(activo=True)
        .select_related("equipo", "estudiante")
        .order_by("fecha_asignacion", "id")
    )

    asignaciones = []
    asignacion_reciente_id = request.session.pop("asignacion_reciente_id", None)
    idx_reciente = None

    # Construimos una lista indexada limpia (sin estudiantes = None)
    for asig in asignaciones_qs:
        if asig.estudiante is None:
            # Asignación vieja o dañada: la saltamos
            continue

        idx = len(asignaciones)
        asignaciones.append(
            {
                "idx": idx,
                "asignacion": asig,
                "equipo": asig.equipo,
                "estudiante": asig.estudiante,
            }
        )
        if asignacion_reciente_id and asig.id == asignacion_reciente_id:
            idx_reciente = idx

    # Si no hay asignaciones activas válidas, mostramos el mensaje amarillo
    if not asignaciones:
        context = {"asignaciones": []}
        return render(request, "diagnostico/evaluar.html", context)

    # Determinar índice actual (desde POST, GET o la última asignación creada)
    if request.method == "POST":
        try:
            idx_actual = int(request.POST.get("idx", "0"))
        except ValueError:
            idx_actual = 0
    else:
        if "idx" in request.GET:
            try:
                idx_actual = int(request.GET.get("idx", "0"))
            except ValueError:
                idx_actual = 0
        elif idx_reciente is not None:
            idx_actual = idx_reciente
        else:
            idx_actual = 0

    # Aseguramos que el índice esté en rango
    if idx_actual < 0 or idx_actual >= len(asignaciones):
        idx_actual = 0

    asignacion_actual = asignaciones[idx_actual]["asignacion"]
    equipo_asignado = asignacion_actual.equipo
    estudiante_asignado = asignacion_actual.estudiante  # OBJETO Estudiante

    if request.method == "POST":
        diagnostico_txt = request.POST.get("diagnostico", "").strip()
        solucion_txt = request.POST.get("solucion", "").strip()
        tipo_solucion = request.POST.get("tipo_solucion", "").strip()  # Preventiva / Correctiva

        if not diagnostico_txt or not solucion_txt or not tipo_solucion:
            messages.error(
                request,
                "Diagnóstico, solución y tipo de solución son obligatorios.",
            )
        else:
            # Armamos el texto final de solución
            solucion_final = f"[{tipo_solucion}] {solucion_txt}"

            # Creamos el diagnóstico, guardando el nombre del estudiante en texto
            Diagnostico.objects.create(
                equipo=equipo_asignado,
                estudiante=estudiante_asignado.nombre,
                diagnostico=diagnostico_txt,
                solucion=solucion_final,
                tipo_solucion=tipo_solucion,
            )

            # Equipo pasa a "Listo para entrega"
            equipo_asignado.estado = "L"
            equipo_asignado.save()

            # Desactivamos la asignación ya diagnosticada
            asignacion_actual.activo = False
            asignacion_actual.save()

            messages.success(request, "Diagnóstico registrado correctamente.")
            return redirect("listado_diagnosticos")

    # Nombre ya formateado para el input de solo lectura
    estudiante_asignado_nombre = estudiante_asignado.nombre if estudiante_asignado else ""

    context = {
        "asignaciones": asignaciones,
        "idx_actual": idx_actual,
        "equipo_asignado": equipo_asignado,
        "estudiante_asignado": estudiante_asignado_nombre,
    }
    return render(request, "diagnostico/evaluar.html", context)


# ------------------ LISTADO DE DIAGNÓSTICOS POR EQUIPO ------------------ #
def listado_diagnosticos(request):
    """
    Seguimiento de equipos y diagnósticos.

    - Muestra todos los equipos que NO han sido entregados (estado != 'E').
    - Un equipo aparece solo una vez.
    - Estudiante:
        * Si tiene diagnóstico: el estudiante del último diagnóstico.
        * Si NO tiene diagnóstico pero sí asignación activa: ese estudiante.
        * Si no tiene nada: 'No asignado'.
    - Último diagnóstico:
        * Texto del último diagnóstico o 'Sin diagnóstico'.
    - Estado visual:
        * R -> Pendiente (rojo)
        * D -> Asignado (amarillo)
        * L -> Para entrega (verde)
    """
    redir = _requerir_login(request)
    if redir:
        return redir

    equipos = Equipo.objects.exclude(estado="E").order_by("fecha_recepcion", "id")
    filas = []

    for equipo in equipos:
        # Último diagnóstico del equipo (si existe)
        ultimo_diag = (
            Diagnostico.objects.filter(equipo=equipo)
            .order_by("-fecha_diagnostico", "-id")
            .first()
        )

        # Estudiante + texto de diagnóstico a mostrar en la tabla
        if ultimo_diag:
            nombre_estudiante = ultimo_diag.estudiante
            texto_diagnostico = ultimo_diag.diagnostico
            ultimo_diag_id = ultimo_diag.id
        else:
            # Si no hay diagnóstico, intentamos ver si hay una asignación activa
            asig = (
                Asignacion.objects.filter(equipo=equipo, activo=True)
                .select_related("estudiante")
                .first()
            )
            if asig and asig.estudiante:
                nombre_estudiante = asig.estudiante.nombre
            else:
                nombre_estudiante = "No asignado"
            texto_diagnostico = "Sin diagnóstico"
            ultimo_diag_id = None

        # Estado lógico + estilo visual
        if equipo.estado == "R":
            estado_logico = "Pendiente"
            estado_badge = "badge bg-danger"
        elif equipo.estado == "D":
            estado_logico = "Asignado"
            estado_badge = "badge bg-warning text-dark"
        elif equipo.estado == "L":
            estado_logico = "Para entrega"
            estado_badge = "badge bg-success"
        else:
            estado_logico = "Sin información"
            estado_badge = "badge bg-secondary"

        filas.append(
            {
                "equipo": equipo,
                "cliente": equipo.nombre,
                "tipo": equipo.tipo,
                "problema": equipo.problema,
                "estudiante": nombre_estudiante,
                "ultimo_diagnostico": texto_diagnostico,
                "ultimo_diagnostico_id": ultimo_diag_id,
                "estado_equipo": estado_logico,
                "estado_badge": estado_badge,
            }
        )

    context = {
        "filas": filas,
    }
    return render(request, "diagnostico/listado.html", context)


# ------------------ CRUD DE DIAGNÓSTICOS (como tal) ------------------ #
def historial_diagnosticos(request):
    """
    Lista TODOS los diagnósticos registrados (CRUD de Diagnóstico – Read).
    """
    redir = _requerir_login(request)
    if redir:
        return redir

    diagnosticos = (
        Diagnostico.objects.select_related("equipo")
        .order_by("-fecha_diagnostico", "-id")
    )
    return render(
        request,
        "diagnostico/historial.html",
        {"diagnosticos": diagnosticos},
    )


def editar_diagnostico(request, diagnostico_id):
    """
    Edita un diagnóstico ya registrado (CRUD de Diagnóstico – Update).
    No permite editar si el equipo ya fue entregado al cliente (estado = 'E').
    """
    redir = _requerir_login(request)
    if redir:
        return redir

    diag = get_object_or_404(Diagnostico, id=diagnostico_id)

    # ⛔ Bloquear edición si el equipo ya fue entregado
    if diag.equipo.estado == "E":
        messages.error(
            request,
            "No se puede editar un equipo ya entregado.",
        )
        return redirect("historial_diagnosticos")

    if request.method == "POST":
        diagnostico_txt = request.POST.get("diagnostico", "").strip()
        tipo_solucion = request.POST.get("tipo_solucion", "").strip()
        solucion_txt = request.POST.get("solucion", "").strip()

        if not diagnostico_txt or not tipo_solucion or not solucion_txt:
            messages.error(
                request,
                "Diagnóstico, tipo de solución y detalle de solución son obligatorios.",
            )
        else:
            # Reconstruimos el texto solución con prefijo [Tipo]
            solucion_final = f"[{tipo_solucion}] {solucion_txt}"

            diag.diagnostico = diagnostico_txt
            diag.tipo_solucion = tipo_solucion
            diag.solucion = solucion_final
            diag.save()

            messages.success(request, "Diagnóstico actualizado correctamente.")
            return redirect("historial_diagnosticos")

    # Para GET, prellenamos usando las propiedades del modelo
    contexto = {
        "diag": diag,
        "equipo": diag.equipo,
        "tipo_solucion": diag.tipo_solucion_desde_texto,
        "solucion_detalle": diag.solucion_detalle,
    }
    return render(request, "diagnostico/diagnostico_form.html", contexto)


def eliminar_diagnostico(request, diagnostico_id):
    """
    Elimina un diagnóstico (CRUD de Diagnóstico – Delete).
    No permite eliminar si el equipo ya fue entregado al cliente (estado = 'E').
    """
    redir = _requerir_login(request)
    if redir:
        return redir

    diag = get_object_or_404(Diagnostico, id=diagnostico_id)

    # ⛔ Bloquear eliminación si el equipo ya fue entregado
    if diag.equipo.estado == "E":
        messages.error(
            request,
            "No se puede eliminar un equipo ya entregado.",
        )
        return redirect("historial_diagnosticos")

    if request.method == "POST":
        diag.delete()
        messages.success(request, "Diagnóstico eliminado correctamente.")
        return redirect("historial_diagnosticos")

    return render(request, "diagnostico/diagnostico_eliminar.html", {"diag": diag})
