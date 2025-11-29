from django.shortcuts import render, redirect
from django.contrib import messages


def login_view(request):
    """
    Login súper simple:
    usuario: inacap
    clave:   clinica2025
    Crea una variable de sesión 'autenticado' cuando el login es correcto.
    """
    # Si ya está autenticado, lo mando directo a recepción
    if request.session.get('autenticado'):
        return redirect('registrar_equipo')

    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        clave = request.POST.get('clave')

        if usuario == 'inacap' and clave == 'clinica2025':
            request.session['autenticado'] = True
            messages.success(request, "Has iniciado sesión correctamente.")
            return redirect('registrar_equipo')
        else:
            messages.error(request, 'Credenciales incorrectas')

    return render(request, 'login/login.html')


def logout_view(request):
    """
    Cierra la sesión y redirige al login.
    """
    request.session.flush()
    return redirect('login')
