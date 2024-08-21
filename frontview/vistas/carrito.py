from django.shortcuts import redirect
from django.views import View
from frontview.models import Productos

class Carrito(View):

    def post(self, request):
        # Obtenemos el producto y la acción (agregar o borrar)
        producto_id = request.POST.get('producto')
        borrar = request.POST.get('borrar')
        carrito = request.session.get('carrito', {})
        
        # Verificamos si ya hay productos en el carrito
        if carrito:
            cantidad = carrito.get(producto_id)
            if cantidad:
                if borrar:
                    if cantidad <= 1:
                        carrito.pop(producto_id)
                    else:
                        carrito[producto_id] = cantidad - 1
                else:
                    carrito[producto_id] = cantidad + 1
            else:
                carrito[producto_id] = 1
        else:
            carrito[producto_id] = 1
        
        # Guardamos el carrito en la sesión
        request.session['carrito'] = carrito
        print(f'Carrito actualizado: {request.session["carrito"]}')
        
        return redirect('carrito')

    def get(self, request):
        return redirect('tienda')


# Función para limpiar el carrito
def limpiar_carrito(request):
    request.session['carrito'] = {}
    return redirect('tienda')