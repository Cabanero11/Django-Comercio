from django.shortcuts import render, redirect 
from frontview.models import Usuario, Productos, Pedido
from django.views import View 


class Cerrar_sesion(View): 
    """
    Manages the session closing process, saving the user's cart as orders.

    This view handles the closure of the user's session by saving the current
    shopping cart as orders in the database and then clearing the cart.

    Methods:
        post(request): Processes the session closure and saves the cart as orders.
    """

    def post(self, request): 
        """
        Handles the session closure, converting the cart items into orders.

        Args:
            request (HttpRequest): The HTTP request containing the user and cart information.

        Returns:
            HttpResponse: Redirects to the homepage after processing the orders and clearing the cart.
        """


        direccion = request.POST.get('direccion')  
        usuario = request.session.get('usuario') 
        carrito = request.session.get('carrito') 
        productos = Productos.get_products_by_id(list(carrito.keys()))  
        
        # Guardar producto, si se cierra sesion
        for producto in productos: 
            print(carrito.get(str(producto.id))) 
            pedido = Pedido(usuario=Usuario(id=usuario), 
                          producto = producto, 
                          precio = producto.precio, 
                          direccion = direccion, 
                          cantidad = carrito.get(str(producto.id))) 
            pedido.save() 

        request.session['carrito'] = {} 
        return redirect('homepage')