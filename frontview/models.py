# Actualizar datos
# python .\manage.py makemigrations
# python .\manage.py migrate

"""
This module contains the data models for the Django application.

It includes the logic for handling the 'frontview' application's data.
"""


from django.db import models
from datetime import datetime

# Modelo de categorias de productos (ropa xd)
class Categoria(models.Model):

    """
    Model representing product categories (clothing).

    Attributes:
        nombre (CharField): Name of the category.
    """

    nombre = models.CharField(max_length=50)

    # Metodo estatico para obtener todas las categorias
    @staticmethod
    def get_all_categorias():
        """
        Retrieve all categories from the database.

        Returns:
            QuerySet: All category records.
        """
        return Categoria.objects.all()
    
    # De momento solo nombre
    def __str__(self):
        """
        String representation of the category object.

        Returns:
            str: Name of the category.
        """
        return self.nombre
    

class Usuario(models.Model):
    """
    Model representing a user in the system.

    Attributes:
        nombre (CharField): First name of the user.
        apellidos (CharField): Last name of the user.
        usuario (CharField): Username, must be unique.
        email (EmailField): Email address, must be unique.
        contraseña (CharField): Password of the user.
        direccion (CharField): Optional address field.
        tefelono (CharField): Optional phone number field.
    """

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
        """
        Registers and saves the user in the database.
        """
        self.save()

    # Si el email le corresponde
    @staticmethod
    def get_usuario_por_email(email):
        """
        Retrieves a user by their email.

        Args:
            email (str): The email address to search for.

        Returns:
            Usuario: The user object if found, or None.
        """

        try:
            return Usuario.objects.get(email=email)
        except Exception as e:
            print(f'Error al encontrar Usuario por email: {e}')
            return None
    
    # Si existe email o usuario ya creado
    def existeUsuario(self):
        """
        Retrieves a user by their email.

        Args:
            email (str): The email address to search for.

        Returns:
            Usuario: The user object if found, or None.
        """

        if Usuario.objects.filter(email=self.email) or Usuario.objects.filter(usuario=self.usuario):
            return True
        else:
            return False


# Tallas de los productos
class Tallas(models.Model):
    """
    Model representing product sizes.

    Attributes:
        nombre (CharField): The size identifier (XS, S, M, ...)
    """

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

        """
        String representation of the size object.

        Returns:
            str: The size acronym (e.g., S, M, L).
        """

        return self.get_nombre_display()



class Productos(models.Model):
    """
    Model representing a product in the system.

    Attributes:
        nombre (CharField): Product name.
        precio (FloatField): Product price.
        categoria (ForeignKey): Category the product belongs to.
        descripcion (CharField): Optional description of the product.
        imagen (ImageField): Image associated with the product.
        tallas (ManyToManyField): Available sizes for the product.
    """


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
        """
        Retrieves all products associated with a specific size.

        Args:
            talla_id (int): The size ID.

        Returns:
            QuerySet: Products associated with the given size.
        """

        return Productos.objects.filter(tallas__id=talla_id)

    # Obtener producto por id
    @staticmethod
    def get_producto_por_id(ids):
        """
        Retrieves a product by its ID.

        Args:
            ids (int): The product ID.

        Returns:
            QuerySet: The product matching the given ID.
        """

        return Productos.objects.filter(id=ids)
    
    # Obtener todos los productos
    @staticmethod
    def get_all_productos():
        """
        Retrieves all products.

        Returns:
            QuerySet: All product records.
        """

        return Productos.objects.all()
    
    # Obtener todos los productos de una categoria
    @staticmethod
    def get_all_productos_categoria(id_categoria):
        """
        Retrieves all products for a specific category.

        Args:
            id_categoria (int): The category ID.

        Returns:
            QuerySet: Products belonging to the given category.
        """

        if id_categoria:
            return Productos.objects.filter(categoria=id_categoria)
        else:
            # Sino esta la categoria devuelvo todos
            return Productos.get_all_productos()


class Pedido(models.Model):
    """
    Model representing an order in the system.

    Attributes:
        producto (ForeignKey): Product associated with the order.
        usuario (ForeignKey): User who placed the order.
        cantidad (IntegerField): Quantity of the product ordered.
        precio (FloatField): Total price of the order.
        direccion (CharField): Shipping address.
        tefelono (CharField): Contact phone number.
        fecha (DateField): Order date.
        estado_pedido (BooleanField): Whether the order is completed.
        talla (CharField): Size of the product ordered.
    """


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
        """
        Creates and saves the order in the database.
        """

        self.save()

    @staticmethod
    def get_pedido_usuario(id_usuario):
        """
        Retrieves all pending orders for a specific user.

        Args:
            id_usuario (int): The user's ID.

        Returns:
            QuerySet: Orders that are not yet completed, sorted by date.
        """
        
        return Pedido.objects.filter(usuario=id_usuario, estado_pedido=False).order_by('-fecha')
    





