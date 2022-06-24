# archivo de creacion de vistas, que tienen el formato de una clase en python
from distutils.log import error
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .models import Company
from django.utils.decorators import method_decorator # import necesario para exonerar la peticino de verificacion
from django.views.decorators.csrf import csrf_exempt # import necesario para exonerar la peticino de verificacion

# Create your views here.

class CompanyView(View):
    # metodo que se ejecuta para despachar una peticion, osea
    # que cada vez que se despache o se envie una respuesta,
    # se va a verificar, y se podra hacer el post
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    # metodo get para obtener la info de la base de datos, en este caso
    # si se especifica en la url un id, sera de ese elemento. Sino
    # la informacion obtenida sera global
    def get(self, request, id=0):
        if (id>0):
            companies=list(Company.objects.filter(id=id).values())
            if len(companies) > 0:
                company=companies[0]
                datos={'message': "Success, here is the company info you asked for", 'company': company}
            else:
                datos={'message': "Company not found"}
            return JsonResponse(datos)
                
        else:
            # se guarda en una variable la informacino obtenida del modelo Company, 
            # se obtienen los valores y se enlistan para poder
            # ser utilizados por Django y convertirlo a Json
            # por esa razon, se parsea todo como list
            companies=list(Company.objects.values()) # ORM -  mapeo objeto relacional
        
            # si el contenido de la base de datos es mayor que cero entonces
            # enviar la enformacion en formato json y retornarla
            if len(companies)>0:
                datos={'message': "Success, here are the companies", 'companies': companies}
            
            else:
                datos={'message': "Companies not found..."} 
            # en este return, se retorna el json de los datos obtenidos
            return JsonResponse(datos)
    
    
    # el post se usa para agregar un elemento a la base de datos
    def post(self, request):
        # request es el parametro en la peticion y el body es el cuerpo ( contenido ) de la peticion
        
        #se convierte en json la peticion hecha del post
        json_data = json.loads(request.body) # el json.loads se usa para convertir una lista a json
        #print(json_data)
        # para crear un elemento para el post y ponerlo en la base de datos
        Company.objects.create(name=json_data['name'],website=json_data['website'],foundation=json_data['foundation'])
        datos={'message': "Success, the post has been done"}    
        return JsonResponse(datos)
    
    
    
    # put se usa para modificar algo en la base de datos con la informacion proporcionada
    def put(self, request,id): 
        json_data = json.loads(request.body) # el json.loads se usa para convertir una lista a json
        companies = list(Company.objects.filter(id=id).values()) # se verifica si existe una company con el id que se pide en la URL
        if len(companies) > 0: # si existe entonces, se procede.
            company=Company.objects.get(id=id) # se obtiene la company por id
            
            # se reemplazan los valores originales por los requestados en el put
            company.name = json_data['name']
            company.website = json_data['website']
            company.foundation = json_data['foundation']
            company.save() # guardar los cambios
            datos = {'message': 'Success, the put has been done'}
            
        else:
            datos={'message': "Sorry, the company was not found"}    
        return JsonResponse(datos) # Put en formato json con los datos planteados en el request al id especificado
    
    
    
    def delete(self, request, id):
        companies = list(Company.objects.filter(id=id).values()) # verificacion de si existe o no el itema borrar
        if len(companies) > 0:
            # se filtran los objetos en la base de datos con la intencion de encontrar uno con ese ID
            # y borrar con el metodo propio del ORM delete()
            Company.objects.filter(id=id).delete() 
            # mensaje de exito
            datos = {'message': 'Success, the delete has been done'}
        else:
            datos = {'message': "Failed, the company you tried to delete, doesn't exists"}
        # siempre tiene que haber un return cuando se habla de una vista
        return JsonResponse(datos)
    
    