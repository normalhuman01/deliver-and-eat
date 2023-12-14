from django.urls import path, re_path
from django.conf.urls import url, include
from .views import *
from cliente import views
from .models import *
app_name = "cliente"

# Url's para cliente
urlpatterns = [
    # Vistas basadas en clases y funciones
    path("", views.Index.as_view(), name="IndexCliente"),
    path("home/", HomeCliente, name="HomeCliente"),

    # Registro de cliente
    path("registro-cliente/", views.RegistroCliente.as_view(),
         name="registro_cliente"),
    path("cerrar-sesion/", views.CerrarSesion.as_view(), name="cerrar_sesion"),
    path("carrito/", CarritoView, name="carrito"),
    path('cart/add/<int:pk>/', views.agregar_al_carrito, name='cart_add'),
    path('cart/item_clear/<int:pk>/', views.quitar_del_carrito, name='item_clear'),
    path('cart/item_clear/confirmar/', views.confirmar, name='confirmar'),
    path('ver_menu/', views.ver_menu, name="ver_menu"),


    path("historial_ordenes/", views.historial_ordenes, name="historial_ordenes"),
    path("ordenes_activas/", views.ordenes_activas, name="ordenes_activas"),


]
