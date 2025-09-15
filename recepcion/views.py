from django.shortcuts import render, redirect

equipos = []

def registrar(request):
    if not request.session.get("autenticado"):
        return redirect("/login/")
    if request.method == "POST":
        cliente = request.POST.get("cliente")
        equipo = request.POST.get("equipo")
        problema = request.POST.get("problema")
        equipos.append({"cliente": cliente, "equipo": equipo, "problema": problema})
        return redirect("/recepcion/listado/")
    return render(request, "recepcion/registrar.html")

def listado(request):
    return render(request, "recepcion/listado.html", {"equipos": equipos})

def detalle(request, nombre):
    equipo = next((e for e in equipos if e["cliente"] == nombre), None)
    return render(request, "recepcion/detalle.html", {"equipo": equipo})
