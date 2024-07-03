from django.shortcuts import render

# Create your views here.

def index(request):

    return render(request, 'cuentas/index.html')

def aperitivos(request):

    return render(request, 'cuentas/aperitivos.html')