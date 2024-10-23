from django.shortcuts import render, get_object_or_404
from frontview.models import Productos
from django.views import View

# Visualizar Productos de la tienda individual
class ProductoVista(View):
    """
    View for displaying individual products from the store.

    Methods:
        get(request): Renders the 'producto.html' template.
        post(request): Retrieves a product by its ID and renders the 'producto.html' page with the product details, or an error message if not found.
                       
    """

    def get(self, request):
        """
        Renders the product page.

        Args:
            request (HttpRequest): The HTTP request.

        Returns:
            HttpResponse: The rendered 'producto.html' page.
        """

        return render(request, 'producto.html')
    
    def post(self, request):
        """
        Handles the product retrieval by its ID and renders the product page with the product details.

        Args:
            request (HttpRequest): The HTTP request containing the product ID.

        Returns:
            HttpResponse: The rendered 'producto.html' page with the product details 
                          or an error message if the product is not found.
        """

        producto_id = request.POST.get('producto')
        if producto_id:
            try:
                producto = get_object_or_404(Productos, id=producto_id)
                return render(request, 'producto.html', {'producto': producto})
            except Exception as e:
                print(f'Error {e} al obtener producto {producto_id}')
        return render(request, 'producto.html', {'error': 'Producto no encontrado'})


