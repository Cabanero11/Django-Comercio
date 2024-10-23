from django.shortcuts import render, redirect 
from frontview.models import Pedido, Productos, Usuario
from django.views import View 
from datetime import datetime


# Visualizar Pedidos de un Usuario
class PedidoVista(View):
    """
    View for displaying a user's orders.

    Retrieves the user's orders from the session and calculates the total cost.

    Methods:
        get(request): Retrieves the user's orders and renders the 'pedidos.html' template.
    """


    def get(self, request):
        """
        Retrieves the user's orders and calculates the total cost.

        Args:
            request (HttpRequest): The HTTP request containing session data.

        Returns:
            HttpResponse: The rendered 'pedidos.html' page with the user's orders and total cost.
        """

        usuario = request.session.get('usuario')
        pedidos = Pedido.get_pedido_usuario(usuario)
        total = sum(item.producto.precio for item in pedidos)
        print(f'Pedidos: {pedidos}\nTotal: {total}')
        return render(request, 'pedidos.html', {'carrito': pedidos, 'total': total})
    

class EnviosVista(View):
    """
    View for displaying the user's pending shipments.

    Retrieves the user's pending orders (not completed) and renders the 'envios.html' template.

    Methods:
        get(request): Retrieves pending orders and renders the 'envios.html' page.
    """

    def get(self, request):
        """
        Retrieves the user's pending shipments and renders the 'envios.html' template.

        Args:
            request (HttpRequest): The HTTP request containing session data.

        Returns:
            HttpResponse: The rendered 'envios.html' page with the user's pending shipments.
        """

        usuario_id = request.session.get('usuario')
        
        # Si no hay usuario en la sesión, redirigir al inicio de sesión
        if not usuario_id:
            return redirect('iniciar_sesion')

        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            return redirect('iniciar_sesion')

        # Obtener los pedidos del usuario, filtrando por los que no han sido completados
        pedidos = Pedido.objects.filter(usuario=usuario, estado_pedido=False)
        
        # Pasar los pedidos al template
        return render(request, 'envios.html', {'productos': pedidos})



# Pasar a pedidos.html, sin borrar el carro
def confirmar_pago(request):
    """
    Calculates the total payment amount based on the user's cart and displays the confirmation page.

    Args:
        request (HttpRequest): The HTTP request containing session data.

    Returns:
        HttpResponse: The rendered 'pedidos.html' page with the cart items and total amount.
    """

    usuario_id = request.session.get('usuario')
    carrito = request.session.get('carrito', {})

    # Recalcular el total para asegurarse de que está actualizado
    total = 0
    items_carrito = []
    for key, cantidad in carrito.items():
        producto_id, talla = key.split('-')
        producto = Productos.objects.get(id=producto_id)
        precio_producto = producto.precio * cantidad 
        total += precio_producto
        items_carrito.append({
            'producto': producto,
            'cantidad': cantidad,
            'precio': producto.precio,
            'talla': talla,
        })

    # Redondear a 2 decimales
    total = round(total, 2)

    return render(request, 'pedidos.html', {'carrito': items_carrito, 'total': total})

# Proceso de pagar, daba error de 2 pedidos :(
def finalizar_pago(request):
    """
    Finalizes the user's payment and creates order records based on the cart items.

    If an existing order for the same product exists, it updates the quantity and price.
    Otherwise, it creates a new order.

    Args:
        request (HttpRequest): The HTTP request containing session data.

    Returns:
        HttpResponse: Redirects to the 'envios' page after successfully creating or updating orders.
    """


    usuario_id = request.session.get('usuario')
    carrito = request.session.get('carrito')
    

    # Si el carrito está vacío, redirigir
    if not carrito:
        return redirect('carrito')  

    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        return redirect('iniciar_sesion') 

    direccion = usuario.direccion  
    telefono = usuario.tefelono  

    for key, cantidad in carrito.items():
        producto_id, talla = key.split('-')
        producto = Productos.objects.get(id=producto_id)

        # Intentar recuperar un pedido existente para el usuario y el producto
        pedido_existente = Pedido.objects.filter(usuario=usuario, producto=producto, talla=talla, estado_pedido=False).first()

        if pedido_existente:
            # Si ya existe un pedido para este producto, actualizamos la cantidad y el precio
            pedido_existente.cantidad += cantidad
            pedido_existente.precio += producto.precio * cantidad
            pedido_existente.save()
        else:
            # Si no existe, creamos un nuevo pedido
            nuevo_pedido = Pedido.objects.create(
                usuario=usuario,
                producto=producto,
                cantidad=cantidad,
                precio=producto.precio * cantidad,
                direccion=direccion,
                tefelono=telefono,
                fecha=datetime.today(),
                estado_pedido=False,
                talla=talla,
            )

    # Limpiar el carrito después de crear los pedidos
    request.session['carrito'] = {}

    return redirect('envios')