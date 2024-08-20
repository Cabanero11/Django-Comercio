from django.shortcuts import render, redirect 
from frontview.models import Pedido  
from django.views import View 


# Visualizar Pedidos de un Usuario
class PedidoVista(View):
    def get(self, request):
        usuario = request.session.get('usuario')
        pedido = Pedido.get_pedido_usuario(usuario)
        print(pedido)
        return render(request, 'pedidos.html', {'pedido': pedido})