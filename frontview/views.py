

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
    return render(request, 'homepage.html')

def iniciar_sesion(request):
    return render(request, 'iniciarsesion.html')

def cerrar_sesion(request):
    return render(request, 'cerrarsesion.html')

def registrar(request):
    return render(request, 'registrar.html')

def tienda(request):
    return render(request, 'pedidos.html')

def carrito(request):
    return render(request, 'carrito.html')

def pedidos(request):
    return render(request, 'pedidos.html')
