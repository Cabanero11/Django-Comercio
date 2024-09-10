from django.shortcuts import render, redirect
from django.views import View
from frontview.models import Productos

class Carrito(View):

    # Añadir al carrito
    def post(self, request):
        producto_id = request.POST.get('producto')
        talla = request.POST.get('talla')
        borrar = request.POST.get('borrar')
        carrito = request.session.get('carrito', {})

        if producto_id is None:
            print('No producto ID')
        else:
            print(f'Producto ID: {producto_id}')

        # Clave producto talla
        key = f"{producto_id}-{talla}"

        if carrito:
            cantidad = carrito.get(key)
            if cantidad:
                if borrar:
                    if cantidad <= 1:
                        carrito.pop(key)
                    else:
                        carrito[key] = cantidad - 1
                else:
                    carrito[key] = cantidad + 1
            else:
                carrito[key] = 1
        else:
            carrito = {key: 1}

        request.session['carrito'] = carrito
        request.session['carrito_contador'] = sum(carrito.values())
        print(f'Carrito actualizado: {request.session["carrito"]}')
        return redirect('tienda')

    # Icono carrito
    def get(self, request):
        carrito = request.session.get('carrito', {})
        productos = []

        for key, cantidad in carrito.items():
            # Separar producto y talla
            producto_id, talla = key.split('-')  
            try:
                producto_id = int(producto_id)
                producto = Productos.objects.get(id=producto_id)
                productos.append({
                    'producto': producto,
                    'cantidad': cantidad,
                    'talla': talla  
                })
            except (ValueError, Productos.DoesNotExist):
                carrito.pop(key)

        request.session['carrito'] = carrito
        request.session['carrito_contador'] = sum(carrito.values())
        print(f'Carrito final: {request.session["carrito"]}')

        return render(request, 'carrito.html', {'productos': productos})


# Función para limpiar el carrito entero
def limpiar_carrito(request):
    # Obtenemos el ID del producto a eliminar
    producto_id = request.POST.get('producto_id')
    
    # Obtenemos el carrito actual
    carrito = request.session.get('carrito', {})
    
    talla = request.POST.get('talla')
    key = f"{producto_id}-{talla}"

    # Eliminamos el producto del carrito si existe
    if key in carrito:
        del carrito[key]
    
    # Guardamos el carrito actualizado en la sesión
    request.session['carrito'] = carrito
    
    # Actualizamos el contador del carrito
    request.session['carrito_contador'] = sum(carrito.values())
    
    return redirect('carrito')



# Incrementar la cantidad del producto que esta en el carrito
def incrementar_producto(request):
    carrito = request.session.get('carrito', {})

    # Obtenemos el ID del producto
    producto_id = request.POST.get('producto_id')

    talla = request.POST.get('talla')

    key = f"{producto_id}-{talla}"

    cantidad = carrito.get(key)

    if cantidad:
        carrito[key] = cantidad + 1
    
    
    print(f'Incrementado {producto_id}')

    # Cambiar a carro actualizado, sin el producto
    request.session['carrito'] = carrito
    request.session['carrito_contador'] = sum(carrito.values())

    return redirect('carrito')

# Decrementar la cantidad del producto que esta en el carrito
def decrementar_producto(request):
    carrito = request.session.get('carrito', {})

    # Obtenemos el ID del producto
    producto_id = request.POST.get('producto_id')

    talla = request.POST.get('talla')

    key = f"{producto_id}-{talla}"

    cantidad = carrito.get(key)

    # -1 si hay 2 elementos solo
    if cantidad > 1:
        carrito[key] = cantidad - 1

    print(f'Decrementado {producto_id}')

    # Cambiar a carro actualizado, sin el producto
    request.session['carrito'] = carrito
    request.session['carrito_contador'] = sum(carrito.values())

    return redirect('carrito')