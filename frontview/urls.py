from django.urls import path
from . import views

# Para asociar urls a las views

# URLConf configuracion del modulo, falta importalo

urlpatterns = [
    # En el base
    path('', views.mostrar_productos, name='mostrar_productos'),
]