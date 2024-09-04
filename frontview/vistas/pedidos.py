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
    

class EnviosVista(View):
    def get(self, request):
        usuario = request.session.get('usuario')
        pedidos = Pedido.get_pedido_usuario(usuario)
        print(f'Pedidos: {pedidos}')
        return render(request, 'pedidos.html', {'carrito': pedidos})



# Pasar a pedidos.html, sin borrar el carro
def confirmar_pago(request):
    usuario_id = request.session.get('usuario')
    carrito = request.session.get('carrito', {})

    # Recalcular el total para asegurarse de que está actualizado
    total = 0
    items_carrito = []
    for item_id, cantidad in carrito.items():
        producto = Productos.objects.get(id=item_id)
        precio_producto = producto.precio * cantidad 
        total += precio_producto
        items_carrito.append({
            'producto': producto,
            'cantidad': cantidad,
            'precio': producto.precio
        })

    return render(request, 'pedidos.html', {'carrito': items_carrito, 'total': total})

# Proceso de pagar, daba error de 2 pedidos :(
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

    for item_id, cantidad in carrito.items():
        producto = Productos.objects.get(id=item_id)

        # Intentar recuperar un pedido existente para el usuario y el producto
        pedido_existente = Pedido.objects.filter(usuario=usuario, producto=producto, estado_pedido=False).first()

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
                estado_pedido=False
            )

    # Limpiar el carrito después de crear los pedidos
    request.session['carrito'] = {}

    return redirect('pedidos')