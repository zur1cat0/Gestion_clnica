from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Validación según los requisitos
        if username == 'inacap' and password == 'clinica2025':
            request.session['autenticado'] = True
            request.session['usuario'] = username
            return redirect('/recepcion/registrar/')
        else:
            messages.error(request, 'Credenciales incorrectas. Use usuario: inacap, clave: clinica2025')
    
    return render(request, 'login/login.html')

def logout_view(request):
    request.session.flush()
    return redirect('/login/')


def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('autenticado', False):
            return redirect('/login/')
        return view_func(request, *args, **kwargs)
    return wrapper