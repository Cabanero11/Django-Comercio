from django.shortcuts import render, redirect, HttpResponseRedirect 
from django.contrib.auth.hashers import check_password 
from frontview.models import Usuario 
from django.views import View 



class IniciarSesion(View):
    """
    View for handling user login.

    Allows users to log in by providing their email and password.
    If a specific URL is provided, redirects to it after a successful login.

    Methods:
        get(request): Renders the login page.
        post(request): Handles login logic and redirects to the appropriate page.
    """

    url = None

    # get y mandar a iniciar_sesion si hay url
    def get(self, request):
        """
        Displays the login page and captures any URL redirection.

        Args:
            request (HttpRequest): The HTTP request containing URL parameters.

        Returns:
            HttpResponse: The rendered login page.
        """

        IniciarSesion.url = request.GET.get('url')
        return render(request, 'iniciar_sesion.html')
    
    def post(self, request): 
        """
        Handles user authentication based on the provided email and password.

        Args:
            request (HttpRequest): The HTTP request containing login details.

        Returns:
            HttpResponse: Redirects to the homepage or the provided URL after a successful login,
            or reloads the login page with an error message if the credentials are invalid.
        """

        email = request.POST.get('email') 
        contraseña = request.POST.get('contraseña') 
        usuario = Usuario.get_usuario_por_email(email) 
        msg_error = None
        if usuario:
            # Si coincide la contraseña 
            flag = check_password(contraseña, usuario.contraseña) 
            print(f'Contraseña: {contraseña} - User contraseña: {usuario.contraseña} - Email: {email}')
            if flag: 
                request.session['usuario'] = usuario.id
                request.session['usuario_nombre'] = usuario.nombre
                # Si hay url de login, sino pal home
                if IniciarSesion.url: 
                    return HttpResponseRedirect(IniciarSesion.url) 
                else: 
                    IniciarSesion.url = None
                    return redirect('homepage') 
            else: 
                msg_error = 'No coindice contraseña !!'
        else: 
            msg_error = 'Error Usuario !!'

        print(f'Usuario: {usuario} {contraseña} inicio sesion') 
        return render(request, 'iniciar_sesion.html', {'error': msg_error})

# Desde el boton de carrito, asi vuelves a carrito y mas comodo
class IniciarSesionCarrito(View):
    """
    View for handling user login specifically from the cart page.

    If a specific URL is provided, it redirects to that URL after a successful login,
    otherwise redirects to the cart.

    Methods:
        get(request): Renders the login page for the cart.
        post(request): Handles login logic and redirects to the cart or the appropriate page.
    """

    url = None

    # get y mandar a iniciar_sesion si hay url
    def get(self, request):
        """
        Displays the cart login page and captures any URL redirection.

        Args:
            request (HttpRequest): The HTTP request containing URL parameters.

        Returns:
            HttpResponse: The rendered cart login page.
        """

        IniciarSesion.url = request.GET.get('url')
        return render(request, 'iniciar_sesion_carrito.html')
    
    def post(self, request):
        """
        Handles user authentication based on the provided email and password
        for accessing the cart.

        Args:
            request (HttpRequest): The HTTP request containing login details.

        Returns:
            HttpResponse: Redirects to the cart page or the provided URL after a successful login,
            or reloads the cart login page with an error message if the credentials are invalid.
        """

        email = request.POST.get('email') 
        contraseña = request.POST.get('contraseña') 
        usuario = Usuario.get_usuario_por_email(email) 
        msg_error = None
        if usuario:
            # Si coincide la contraseña 
            flag = check_password(contraseña, usuario.contraseña) 
            print(f'Contraseña: {contraseña} - User contraseña: {usuario.contraseña} - Email: {email}')
            if flag: 
                request.session['usuario'] = usuario.id
                request.session['usuario_nombre'] = usuario.nombre
                # Si hay url de login, sino pal home
                if IniciarSesion.url: 
                    return HttpResponseRedirect(IniciarSesion.url) 
                else: 
                    IniciarSesion.url = None
                    return redirect('carrito') 
            else: 
                msg_error = 'No coindice contraseña !!'
        else: 
            msg_error = 'Error Usuario !!'

        print(f'Usuario: {usuario} {contraseña} inicio sesion') 
        return render(request, 'iniciar_sesion_carrito.html', {'error': msg_error})  


class PerfilUsuario(View):
    """
    View for displaying the user's profile page.

    Displays the user's profile information if they are authenticated.

    Methods:
        get(request): Retrieves and displays the user's profile.
    """

    def get(self, request):
        """
        Displays the user's profile if they are authenticated.

        Args:
            request (HttpRequest): The HTTP request containing session data.

        Returns:
            HttpResponse: The rendered user profile page, or a redirect to the login page if the user is not authenticated.
        """

        # Obtiene el ID del usuario desde la sesión
        usuario_id = request.session.get('usuario')

        # Verifica si el usuario está autenticado (si tiene un ID en la sesión)
        if not usuario_id:
            # Redirecciona al login si no está autenticado
            return redirect('iniciar_sesion')

        # Intenta obtener el usuario desde la base de datos
        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            # Si no existe el usuario, redirecciona al login
            return redirect('iniciar_sesion')

        print(f'Perfil {usuario.nombre} accedió a su perfil.')

        # Pasa los datos del usuario al template
        return render(request, 'usuario.html', {'usuario': usuario})


# Te manda al login otra vez
def cerrar_sesion(request):
    """
    Logs the user out by clearing the session and redirects to the login page.

    Args:
        request (HttpRequest): The HTTP request that initiates the logout.

    Returns:
        HttpResponse: Redirects to the login page after clearing the session.
    """

    request.session.clear()
    return redirect('iniciar_sesion')



