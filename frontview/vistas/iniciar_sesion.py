from django.shortcuts import render, redirect, HttpResponseRedirect 
from django.contrib.auth.hashers import check_password 
from frontview.models import Usuario 
from django.views import View 



class IniciarSesion(View):
    url = None

    # get y mandar a iniciar_sesion si hay url
    def get(self, request):
        IniciarSesion.url = request.GET.get('url')
        return render(request, 'iniciar_sesion.html')
    
    def post(self, request): 
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
    
# Te manda al login otra vez
def cerrar_sesion(request):
    request.session.clear()
    return redirect('iniciar_sesion')