from django.shortcuts import render

def index(request):
    return render(request, 'cuentas/index.html')

def aperitivos(request):
    return render(request, 'cuentas/aperitivos.html')

def comida(request):
    return render(request, 'cuentas/comida.html')

def batidos(request):
    return render(request, 'cuentas/batidos.html')

def contacto(request):
    return render(request, 'cuentas/contacto.html')

def login(request):
    return render(request, 'cuentas/login.html')

def registro(request):
    return render(request, 'cuentas/registro.html')

def olvido_contraseña(request):
    return render(request, 'cuentas/olvido-contraseña.html')
