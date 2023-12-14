from django.urls import path
from django.conf.urls import url, include

from administrador import views
from .views import *
import repartidor 
from repartidor import views 
app_name = "administrador"

urlpatterns = [

    # temporal, no se llamarán así las vistas
    path("", index, name="IndexAdministrador"),
    # ruta para listar las ordenes con vistas basadas en funciones
    path("lista-ordenes/", lista_ordenes, name="listar_ordenes"),
    # ruta para editar una orden, recibe el id de la orden a editar en la url
    path("editar-ordenes/(?P<pk>d+)/", editar_orden, name="editar_orden"),
    # ruta para eliminar una orden, recibe el id de la orden a eliminar en la url
    path("eliminar-ordenes/(?P<pk>d+)/", eliminar_orden, name="eliminar_orden"),

]
