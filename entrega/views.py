from django.shortcuts import render, redirect

reportes = []

def verificar(request):
    if request.method == "GET":
        cliente = request.GET.get("cliente")
        equipo = next((r for r in reportes if r["cliente"] == cliente), None)
        return render(request, "entrega/verificar.html", {"equipo": equipo})
    return render(request, "entrega/verificar.html")

def reporte(request):
    if request.method == "POST":
        cliente = request.POST.get("cliente")
        estado = request.POST.get("estado")
        obs = request.POST.get("observaciones")
        reportes.append({"cliente": cliente, "estado": estado, "obs": obs})
        return redirect("/entrega/comprobante/")
    return render(request, "entrega/reporte.html")

def comprobante(request):
    if reportes:
        ultimo = reportes[-1]
        return render(request, "entrega/comprobante.html", {"reporte": ultimo})
    return render(request, "entrega/comprobante.html")
