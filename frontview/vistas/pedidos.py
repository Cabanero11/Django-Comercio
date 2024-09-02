from django.shortcuts import render, redirect 
from frontview.models import Pedido, Productos, Usuario
from django.views import View 
from datetime import datetime


# Visualizar Pedidos de un Usuario
class PedidoVista(View):
    def get(self, request):
        usuario = request.session.get('usuario')
        pedidos = Pedido.get_pedido_usuario(usuario)
        total = sum(item.producto.precio for item in pedidos)
        print(f'Pedidos: {pedidos}\nTotal: {total}')
        return render(request, 'pedidos.html', {'carrito': pedidos, 'total': total})


# Proceso de pagar
def finalizar_pago(request):
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

        # Crear un pedido por cada producto en el carrito
        for item_id, cantidad in carrito.items():
            producto = Productos.objects.get(id=item_id)
            # Para evitar duplicacion de carritos, y acumulacion de productos
            # Revisar si esta o no creado
            pedido, created = Pedido.objects.get_or_create(
            usuario=usuario,
            producto=producto,
            defaults={
                'cantidad': cantidad,
                'precio': producto.precio * cantidad,
                'direccion': direccion,
                'tefelono': telefono,
                'fecha': datetime.today(),
                'estado_pedido': False
            }
        )
        if not created:
            # Si el pedido existe, actualizar la cantidad y el precio
            pedido.cantidad += cantidad
            pedido.precio += producto.precio * cantidad
            pedido.save()

        # Limpiar el carrito después de crear los pedidos
        request.session['carrito'] = {}

        return redirect('pedidos')