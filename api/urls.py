from django.urls import path
from .views import CompanyView

urlpatterns = [
    path('companies/',CompanyView.as_view(),name='companies_list'), # esto da el total de las companies almacenadas en la base de datos 
    path('companies/<int:id>',CompanyView.as_view(),name='companies_process') # esta url daria la companie con el ID especificado en el URL
]
