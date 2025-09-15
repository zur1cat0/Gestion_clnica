from django.shortcuts import render, redirect
from django.contrib import messages
from login.views import login_required

# Simulación de base de datos con lista de diccionarios
equipos_recibidos = []

@login_required  
def registrar_equipo(request):
    if request.method == 'POST':
        nombre_cliente = request.POST.get('nombre_cliente', '').strip()
        tipo_equipo = request.POST.get('tipo_equipo', '').strip() 
        problema = request.POST.get('problema', '').strip()
        
        if nombre_cliente and tipo_equipo and problema:
            equipo = {
                'id': len(equipos_recibidos) + 1,
                'nombre_cliente': nombre_cliente,
                'tipo_equipo': tipo_equipo,
                'problema': problema,
                'estado': 'Recibido'
            }
            equipos_recibidos.append(equipo)
            messages.success(request, f'Equipo de {nombre_cliente} registrado correctamente.')
            return redirect('/recepcion/listado/')
        else:
            messages.error(request, 'Todos los campos son obligatorios.')
    
    return render(request, 'recepcion/registrar.html')

@login_required
def listado_equipos(request):
    context = {'equipos': equipos_recibidos}
    return render(request, 'recepcion/listado.html', context)

@login_required
def detalle_equipo(request, nombre):
    equipo = None
    for eq in equipos_recibidos:
        if eq['nombre_cliente'].lower() == nombre.lower():
            equipo = eq
            break
    
    if not equipo:
        messages.error(request, 'Equipo no encontrado.')
        return redirect('/recepcion/listado/')
    
    context = {'equipo': equipo}
    return render(request, 'recepcion/detalle.html', context)