from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    """Vista de login según especificaciones de la evaluación"""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        # Validar credenciales según evaluación
        if username == 'inacap' and password == 'clinica2025':
            # Autenticación exitosa
            request.session['autenticado'] = True
            request.session['usuario'] = username
            
            messages.success(request, f'¡Bienvenido {username}!')
            return redirect('recepcion:registrar') # ← Según evaluación
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'login/login.html')

def logout_view(request):
    """Vista para cerrar sesión"""
    request.session.flush()
    messages.info(request, 'Has cerrado sesión correctamente')
    return redirect('login:login')