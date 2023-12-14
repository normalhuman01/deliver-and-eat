from administrador.views import superuser_only
from django.conf.urls import url,include
from django.urls import path
from . import views
from .views import *

app_name = "repartidor"

urlpatterns = [
    path("", index_repartidor, name="index_repartidor"),
    path("registro-repartidor/", superuser_only(views.RegistroRepartidor.as_view()), name="registro-repartidor"),
    path("ordenes-para-recoleccion/", ordenes_para_recoleccion, name="ordenes_para_recoleccion"),
    path("comenzar_entrega/(?P<pk>d+)/", comenzar_entrega, name="comenzar_entrega"),
    path("ordenes-asignadas/", ordenes_asignadas, name="ordenes_asignadas"),
    path("finalizar_entrega/(?P<pk>d+)/", finalizar_entrega, name="finalizar_entrega"),
    path("ordenes-realizadas/", ordenes_realizadas, name="ordenes_realizadas"),
]