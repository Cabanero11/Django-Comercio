# Actualizar datos
# python .\manage.py makemigrations
# python .\manage.py migrate

"""
Este módulo contiene los modulos para la aplicación Django.

Contiene la lógica de los datos de la aplicación 'frontview'.
"""


from django.db import models
from datetime import datetime

# Modelo de categorias de productos (ropa xd)
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    # Metodo estatico para obtener todas las categorias
    @staticmethod
    def get_all_categorias():
        return Categoria.objects.all()
    
    # De momento solo nombre
    def __str__(self):
        return self.nombre
    

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=60)
    usuario = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=100)
    # Finalizar pedido
    direccion = models.CharField(max_length=100, default='', blank=True)
    tefelono = models.CharField(max_length=9, default='', blank=True)

    # Se registra y guarda en la BD (SQlite)
    def regristrar(self):
        self.save()

    # Si el email le corresponde
    @staticmethod
    def get_usuario_por_email(email):
        try:
            return Usuario.objects.get(email=email)
        except Exception as e:
            print(f'Error al encontrar Usuario por email: {e}')
            return None
    
    # Si existe email o usuario ya creado
    def existeUsuario(self):
        if Usuario.objects.filter(email=self.email) or Usuario.objects.filter(usuario=self.usuario):
            return True
        else:
            return False


# Tallas de los productos
class Tallas(models.Model):
    lista_tallas = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Extra Extra Large'),
    ]

    nombre = models.CharField(max_length=3, choices=lista_tallas, unique=True)

    # Devolver acronimo de la Talla
    def __str__(self):
        return self.get_nombre_display()



class Productos(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.FloatField(default=0)
    # Añadir como id la categoria al producto
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, default=1)
    descripcion = models.CharField(
        max_length=200, default='', blank=True, null=True
    )
    # Las imagenes se guardan en uploads/productos
    imagen = models.ImageField(upload_to='productos/')

    tallas = models.ManyToManyField(Tallas)

    # Obtener productos por talla
    @staticmethod
    def get_productos_por_talla(talla_id):
        return Productos.objects.filter(tallas__id=talla_id)

    # Obtener producto por id
    @staticmethod
    def get_producto_por_id(ids):
        return Productos.objects.filter(id=ids)
    
    # Obtener todos los productos
    @staticmethod
    def get_all_productos():
        return Productos.objects.all()
    
    # Obtener todos los productos de una categoria
    @staticmethod
    def get_all_productos_categoria(id_categoria):
        if id_categoria:
            return Productos.objects.filter(categoria=id_categoria)
        else:
            # Sino esta la categoria devuelvo todos
            return Productos.get_all_productos()


class Pedido(models.Model):
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio = models.FloatField()
    direccion = models.CharField(max_length=100, default='', blank=True)
    tefelono = models.CharField(max_length=9, default='', blank=True)
    fecha = models.DateField(default=datetime.today)
    estado_pedido = models.BooleanField(default=False)
    talla = models.CharField(max_length=20, default='M')

    # Crear pedido en BD
    def crearPedido(self):
        self.save()

    @staticmethod
    def get_pedido_usuario(id_usuario):
        return Pedido.objects.filter(usuario=id_usuario, estado_pedido=False).order_by('-fecha')
    





