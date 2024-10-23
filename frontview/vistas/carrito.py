from django.shortcuts import render, redirect
from django.views import View
from frontview.models import Productos

"""
View for the shopping cart to add, remove products and view the cart.
"""

class Carrito(View):
    """
    Manages the shopping cart actions such as adding and removing products.
    """

    # Añadir al carrito
    def post(self, request):
        """
        Adds a product to the cart or removes it based on the request.

        Args:
            request (HttpRequest): The HTTP request containing the product and action.

        Returns:
            HttpResponse: Redirects to the store page after updating the cart.
        """


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
        """
        Retrieves and displays the shopping cart.

        Args:
            request (HttpRequest): The HTTP request.

        Returns:
            HttpResponse: Renders the shopping cart page with the list of products.
        """

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
    """
    Clears the entire shopping cart or removes a specific product.

    Args:
        request (HttpRequest): The HTTP request containing the product to be removed.

    Returns:
        HttpResponse: Redirects to the cart page after clearing the cart.
    """


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
    """
    Increments the quantity of a product in the cart.

    Args:
        request (HttpRequest): The HTTP request containing the product to be incremented.

    Returns:
        HttpResponse: Redirects to the cart page after updating the quantity.
    """

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
    """
    Decrements the quantity of a product in the cart, removing it if the quantity is 1.

    Args:
        request (HttpRequest): The HTTP request containing the product to be decremented.

    Returns:
        HttpResponse: Redirects to the cart page after updating the quantity.
    """


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