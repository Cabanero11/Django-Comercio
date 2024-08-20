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
        contraseña = request.POST.get('password') 
        usuario = Usuario.get_customer_by_email(email) 
        msg_error = None
        if usuario:
            # Si coincide la contraseña 
            flag = check_password(contraseña, usuario.password) 
            if flag: 
                request.session['usuario'] = usuario.id
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

        print(f'User: {usuario} {contraseña}') 
        return render(request, 'iniciar_sesion.html', {'error': msg_error}) 
    
# Te manda al login otra vez
def cerrar_sesion(request):
    request.session.clear()
    return redirect('login')