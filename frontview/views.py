from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


def mostrar_productos(request):
    return render(request, 'frontview.html')


