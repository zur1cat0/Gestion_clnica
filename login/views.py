from django.shortcuts import render, redirect

def login_view(request):
    error = None
    if request.method == "POST":
        usuario = request.POST.get("usuario")
        clave = request.POST.get("clave")
        if usuario == "inacap" and clave == "clinica2025":
            request.session["autenticado"] = True
            return redirect("/recepcion/registrar/")
        else:
            error = "Usuario o clave incorrectos"
    return render(request, "login/login.html", {"error": error})
