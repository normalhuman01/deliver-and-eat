from django.urls import path
from django.conf.urls import url, include
from .views import *

app_name = "categoria"

# Url's de categorías
urlpatterns = [
    # temporal el index
    path("", Index.as_view(), name="IndexCategoria"),
    # Vistas basadas en funciones
    path("crear-categoria/", crear_categoria, name="crear_categoria"),
    path("ver-categorias/", lista_categoria, name="listar_categorias"),
    path("eliminar_categoria/", eliminar_categoria, name="eliminar_categoria"),
    path("editar_categoria/", editar_categoria, name="editar_categoria"),
    path("selecciona_categoria/", selecciona_categoria, name="selecciona_categoria"),

]
