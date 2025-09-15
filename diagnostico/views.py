from django.shortcuts import render, redirect

diagnosticos = []

def asignar(request):
    if request.method == "GET":
        return render(request, "diagnostico/asignar.html")

def evaluar(request):
    if request.method == "POST":
        estudiante = request.POST.get("estudiante")
        equipo = request.POST.get("equipo")
        diag = request.POST.get("diagnostico")
        solucion = request.POST.get("solucion")
        tipo = "Correctiva" if "reparar" in solucion.lower() else "Preventiva"
        diagnosticos.append({
            "estudiante": estudiante,
            "equipo": equipo,
            "diagnostico": diag,
            "solucion": solucion,
            "tipo": tipo,
        })
        return redirect("/diagnostico/listado/")
    return render(request, "diagnostico/evaluar.html")

def listado(request):
    return render(request, "diagnostico/listado.html", {"diagnosticos": diagnosticos})
