from django.shortcuts import render, redirect
from django.contrib import messages
from login.views import login_required
from recepcion.views import equipos_recibidos
from diagnostico.views import diagnosticos

# Simulación de base de datos para entregas
entregas = []

@login_required
def verificar_equipo(request):
    equipo_encontrado = None
    if request.method == 'GET' and 'cliente' in request.GET:
        nombre_cliente = request.GET.get('cliente')
        
        # Buscar equipo del cliente
        for eq in equipos_recibidos:
            if eq['nombre_cliente'].lower() == nombre_cliente.lower():
                equipo_encontrado = eq
                # Buscar diagnóstico asociado
                for diag in diagnosticos:
                    if diag['equipo']['id'] == eq['id']:
                        equipo_encontrado['diagnostico'] = diag
                        break
                break
        
        if not equipo_encontrado:
            messages.error(request, 'Cliente no encontrado.')
    
    context = {'equipo': equipo_encontrado}
    return render(request, 'entrega/verificar.html', context)

@login_required
def reporte_entrega(request):
    if request.method == 'POST':
        equipo_id = request.POST.get('equipo_id')
        estado_final = request.POST.get('estado_final')
        observaciones = request.POST.get('observaciones', '')
        
        if equipo_id and estado_final:
            entrega = {
                'id': len(entregas) + 1,
                'equipo_id': equipo_id,
                'estado_final': estado_final,
                'observaciones': observaciones,
                'fecha_entrega': 'Hoy'  # En proyecto real usaría datetime
            }
            entregas.append(entrega)
            messages.success(request, 'Reporte de entrega registrado.')
            return redirect('/entrega/comprobante/')
    
    context = {'equipos': equipos_recibidos, 'diagnosticos': diagnosticos}
    return render(request, 'entrega/reporte.html', context)

@login_required
def comprobante_entrega(request):
    # Mostrar último comprobante creado
    comprobante = None
    if entregas:
        ultima_entrega = entregas[-1]
        # Buscar datos completos
        for eq in equipos_recibidos:
            if str(eq['id']) == ultima_entrega['equipo_id']:
                comprobante = {
                    'equipo': eq,
                    'entrega': ultima_entrega
                }
                # Buscar diagnóstico
                for diag in diagnosticos:
                    if diag['equipo']['id'] == eq['id']:
                        comprobante['diagnostico'] = diag
                        break
                break
    
    context = {'comprobante': comprobante}
    return render(request, 'entrega/comprobante.html', context)