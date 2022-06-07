from django.contrib import admin
from .models import Company # se importa el modelo Company para el api y que se registre en el admin

# Register your models here.

admin.site.register(Company) # registrar el company