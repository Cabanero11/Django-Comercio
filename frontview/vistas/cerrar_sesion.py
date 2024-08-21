from django.shortcuts import render, redirect 
from frontview.models import Usuario, Productos, Pedido
from django.views import View 


class Cerrar_sesion(View): 
    def post(self, request): 
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