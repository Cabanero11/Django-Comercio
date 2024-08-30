from django.shortcuts import render, redirect
from django.views import View
from frontview.models import Productos

class Carrito(View):

    # Añadir al carrito
    def post(self, request):
        producto_id = request.POST.get('producto')
        borrar = request.POST.get('borrar')
        carrito = request.session.get('carrito', {})

        if producto_id is None:
            print('No producto ID')
        else:
            print(f'Producto ID: {producto_id}')

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
            carrito = {producto_id: 1}

        request.session['carrito'] = carrito
        request.session['carrito_contador'] = sum(carrito.values())
        print(f'Carrito actualizado: {request.session["carrito"]}')
        return redirect('tienda')

    # Icono carrito
    def get(self, request):
        carrito = request.session.get('carrito', {})
        productos = []

        for producto_id, cantidad in carrito.items():
            try:
                producto_id = int(producto_id)
                producto = Productos.objects.get(id=producto_id)
                productos.append({
                    'producto': producto,
                    'cantidad': cantidad,
                })
            except (ValueError, Productos.DoesNotExist):
                carrito.pop(producto_id)

        request.session['carrito'] = carrito
        request.session['carrito_contador'] = sum(carrito.values())
        print(f'Carrito final: {request.session["carrito"]}')

        return render(request, 'carrito.html', {'productos': productos})


# Función para limpiar el carrito
def limpiar_carrito(request):
    # Obtenemos el ID del producto a eliminar
    producto_id = request.POST.get('producto_id')
    
    # Obtenemos el carrito actual
    carrito = request.session.get('carrito', {})
    
    # Eliminamos el producto del carrito si existe
    if producto_id in carrito:
        del carrito[producto_id]
    
    # Guardamos el carrito actualizado en la sesión
    request.session['carrito'] = carrito
    
    # Actualizamos el contador del carrito
    request.session['carrito_contador'] = sum(carrito.values())
    
    return redirect('carrito')

def limpiar_producto_carro(request, producto_id):
    carrito = request.session.get('carrito', {})

    if producto_id in carrito:
        carrito.pop(producto_id)

    print(f'Eliminado {producto_id}')

    # Cambiar a carro actualizado, sin el producto
    request.session['carrito'] = carrito
    request.session['carrito_contador'] = sum(carrito.values())

    return redirect('carrito')