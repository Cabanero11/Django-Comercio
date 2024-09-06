from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from frontview.models import Productos, Categoria
from django.views import View

# Esta vista sirve para gestionar una tienda online
# Con sus metodos tipicos


class Index(View):

    def post(self, request):
        producto = request.POST.get('producto')
        borrar = request.POST.get('borrar')
        carrito = request.POST.get('carrito')
        
        # Comprobar si hay carrito, producto y sus atributos
        if carrito:
            cantidad = carrito.get(producto)
            if cantidad:
                # Si se compra 1 producto
                if borrar:
                    # default = 1
                    if cantidad <= 1:
                        # Sacamos 1
                        carrito.pop(producto)
                    else:
                        # Sino le quitamos la cantidad
                        carrito[producto] = cantidad - 1
                else: 
                    # Sino se borra, añadimos 1
                    carrito[producto] = cantidad + 1
            else: 
                # Sino hay cantidad, ponemos que es 1
                carrito[producto] = 1
        else:
            carrito = {} # Vacio
            carrito[producto] = 1

        # Creamos sesion, e printeamos
        request.session['carrito'] = carrito
        # Contador de elementos del carrito
        request.session['carrito_contador'] = sum(carrito.values())
        print('carrito', request.session['cart'])
        
        return redirect('homepage')
    
    # Get
    def get(self, request):
        # Para re
        if request.GET.get('action') == 'redirect_to_tienda':
            return HttpResponseRedirect('/tienda')
        return render(request, 'homepage.html')
    

# Fuera de Index
def tienda(request):
    carrito = request.session.get('carrito')
    # No carro, no sesion :p
    if not carrito:
        request.session['carrito'] = {}
        request.session['carrito_contador'] = 0 # Crear contador del carrito

    productos = None
    productos_aleatorios = []
    categorias = Categoria.get_all_categorias()
    id_categoria = request.GET.get('categoria')

    # Obtener los productos
    if id_categoria:
        productos = Productos.get_all_productos_categoria(id_categoria)
        # 5 Productos aleatorios para usar el carousel
        productos_aleatorios = Productos.objects.order_by('?')[:5]
    else:
        # Sin categoria
        productos = Productos.get_all_productos()
        productos_aleatorios = Productos.objects.order_by('?')[:5]

    data = {}
    data['productos'] = productos
    data['productos_aleatorios'] = productos_aleatorios
    data['categorias'] = categorias
    data['carrito_contador'] = request.session.get('carrito_contador', 0)
    print(f'Carrito cont: {request.session.get('carrito_contador')}')

    print(f'Usuario_id home page: {request.session.get('usuario')}')

    return render(request, 'tienda.html', data)