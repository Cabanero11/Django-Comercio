# Crear admin

# python .\manage.py createsuperuser

# caba
# pruebaelqueso

from django.contrib import admin
from .models import *
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered

# Obtener y registrar todos los modelos
modelos = apps.get_models()

for modelo in modelos:
    try:
        admin.site.register(modelo)
    # Cogiendo todos, Group sale registrado, asi lo ignoramos
    except AlreadyRegistered:
        pass
