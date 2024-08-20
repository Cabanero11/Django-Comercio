from django.urls import path
from . import views
from frontview.vistas.home_page import Index, tienda
from frontview.vistas.iniciar_sesion import IniciarSesion, cerrar_sesion
from frontview.vistas.carrito import Carrito
from frontview.vistas.registrar import Registrar
from frontview.vistas.cerrar_sesion import Cerrar_sesion
from frontview.vistas.pedidos import PedidoVista

# Para asociar urls a las views
# URLConf configuracion del modulo, falta importalo

urlpatterns = [
    # En el base
    path('', Index.as_view(), name='homepage'),
    path('tienda', tienda, name='tienda'),

    path('iniciar_sesion', IniciarSesion.as_view(), name='iniciar_sesion'),
    path('cerrar_sesion', cerrar_sesion, name='cerrar_sesion'),
    path('registrar', Registrar.as_view(), name='registrar'),

    path('cerrar', Cerrar_sesion.as_view(), name='cerrar_sesion'),
    path('carrito', Carrito.as_view(), name='carrito'),
    path('pedidos', PedidoVista.as_view(), name='pedidos'),
]