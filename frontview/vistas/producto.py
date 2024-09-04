from django.shortcuts import render, get_object_or_404
from frontview.models import Productos
from django.views import View


# Visualizar Productos de la tienda individual
class ProductoVista(View):
    def get(self, request):
        return render(request, 'producto.html')
    
    def post(self, request):
        producto_id = request.POST.get('producto')
        if producto_id:
            try:
                producto = get_object_or_404(Productos, id=producto_id)
                return render(request, 'producto.html', {'producto': producto})
            except Exception as e:
                print(f'Error {e} al obtener producto {producto_id}')
        return render(request, 'producto.html', {'error': 'Producto no encontrado'})


