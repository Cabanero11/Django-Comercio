from django.urls import path
from . import views
from frontview.vistas.home_page import Index, tienda
from frontview.vistas.iniciar_sesion import IniciarSesion, cerrar_sesion, IniciarSesionCarrito
from frontview.vistas.carrito import Carrito, limpiar_carrito, incrementar_producto, decrementar_producto
from frontview.vistas.registrar import Registrar
from frontview.vistas.cerrar_sesion import Cerrar_sesion
from frontview.vistas.producto import ProductoVista
from frontview.vistas.pedidos import PedidoVista, finalizar_pago, confirmar_pago, EnviosVista

# Para asociar urls a las views
# URLConf configuracion del modulo, falta importalo

urlpatterns = [
    # En el base
    path('', Index.as_view(), name='homepage'),
    path('tienda', tienda, name='tienda'),

    path('iniciar_sesion', IniciarSesion.as_view(), name='iniciar_sesion'),
    path('iniciar_sesion_carrito', IniciarSesionCarrito.as_view(), name='iniciar_sesion_carrito'),
    path('cerrar', cerrar_sesion, name='cerrar_sesion'),
    path('registrar', Registrar.as_view(), name='registrar'),
    
    path('producto_info', ProductoVista.as_view(), name='producto_info'),
    path('cerrar', Cerrar_sesion.as_view(), name='cerrar_sesion'),
    path('carrito', Carrito.as_view(), name='carrito'),
    path('limpiar_carrito', limpiar_carrito, name='limpiar_carrito'),
    path('incrementar_producto', incrementar_producto, name='incrementar_producto'),
    path('decrementar_producto', decrementar_producto, name='decrementar_producto'),
    path('pedidos', PedidoVista.as_view(), name='pedidos'),
    path('envios', EnviosVista.as_view(), name='envios'),
    path('confirmar_pago', confirmar_pago, name='confirmar_pago'),
    path('finalizar_pedidos', finalizar_pago, name='finalizar_pedido')
]