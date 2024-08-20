from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from frontview.models import Usuario
from django.views import View


class Registrar(View):
    
    def get(self, request):
        return render(request, 'registrar.html')
    
    def post(self, request):
        # Obtener datos del 'Usuario'
        post_data = request.POST
        nombre = post_data.get('nombre')
        apellidos = post_data.get('apellidos')
        usuario = post_data.get('usuario')
        email = post_data.get('email')
        contraseña = post_data.get('contraseña')

        # Datos validacion
        datos_usuario = {
            'nombre': nombre,
            'apellidos': apellidos,
            'usuario': usuario,
            'email': email
        }

        msg_error = None
        
        user = Usuario(nombre=nombre, apellidos=apellidos,
                       usuario=usuario, email=email, 
                       contraseña=contraseña)
        
        msg_error = self.validarUsuario()

        if not msg_error:
            # Crear contraseña sino usuario, con django auth
            user.contraseña = make_password(user.contraseña)
            return redirect('homepage')
        else:
            datos_registrar = {
                'error': msg_error,
                'datos_usuario': datos_usuario
            }
            return render(request, 'registrar.html', datos_registrar)

    # Mensajes de error posibles creo
    def validarUsuario(self, user):
        msg_error = None
        if (not user.first_name): 
            msg_error = "Por favor introduce un nombre !!"
        elif len(user.first_name) < 3: 
            msg_error = 'Nombre debe tener mas de 3 caracteres'
        elif not user.last_name: 
            msg_error = 'Porfa pon tus apellidos'
        elif len(user.last_name) < 3: 
            msg_error = 'Tus apellidos deben tener mas de 3 caracteres'
        elif not user.usuario: 
            msg_error = 'Porfa pon nombre Usuario chulo'
        elif len(user.usuario) < 15: 
            msg_error = 'Usuario debe tener menos de 15 caracteres'
        elif len(user.password) < 5: 
            msg_error = 'Contraseña muy corta, minmo 5 caracteres'
        elif len(user.email) < 5: 
            msg_error = 'Email tiene que ser mas de 5 caracteres'
        elif user.isExists(): 
            msg_error = 'Ya esta registrado ese email...'

        return msg_error
