from django.shortcuts import render, redirect
from django.contrib import messages
from login.views import login_required
from recepcion.views import equipos_recibidos

# Simulación de base de datos para diagnósticos
diagnosticos = []

@login_required
def asignar_estudiante(request):
    if request.method == 'GET':
        estudiante = request.GET.get('estudiante')
        equipo_id = request.GET.get('equipo_id')
        
        if estudiante and equipo_id:
            # Buscar equipo
            equipo = None
            for eq in equipos_recibidos:
                if str(eq['id']) == equipo_id:
                    equipo = eq
                    break
            
            if equipo:
                asignacion = {
                    'id': len(diagnosticos) + 1,
                    'estudiante': estudiante,
                    'equipo': equipo,
                    'estado': 'Asignado'
                }
                diagnosticos.append(asignacion)
                messages.success(request, f'Equipo asignado a {estudiante}')
    
    context = {'equipos': equipos_recibidos}
    return render(request, 'diagnostico/asignar.html', context)

@login_required
def evaluar_equipo(request):
    if request.method == 'POST':
        diagnostico_id = request.POST.get('diagnostico_id')
        diagnostico_realizado = request.POST.get('diagnostico')
        solucion = request.POST.get('solucion')
        tipo_solucion = request.POST.get('tipo_solucion')
        
        if diagnostico_id and diagnostico_realizado and solucion:
            # Actualizar diagnóstico
            for diag in diagnosticos:
                if str(diag['id']) == diagnostico_id:
                    diag.update({
                        'diagnostico': diagnostico_realizado,
                        'solucion': solucion,
                        'tipo_solucion': tipo_solucion,
                        'estado': 'Diagnosticado'
                    })
                    break
            messages.success(request, 'Diagnóstico registrado correctamente.')
            return redirect('/diagnostico/listado/')
    
    context = {'diagnosticos': diagnosticos}
    return render(request, 'diagnostico/evaluar.html', context)

@login_required
def listado_diagnosticos(request):
    context = {'diagnosticos': diagnosticos}
    return render(request, 'diagnostico/listado.html', context)