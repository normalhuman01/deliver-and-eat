from django.views import View
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import *
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from .models import *
from .forms import *
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from cliente.models import *
from platillo.models import *
def superuser_only(function):
    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return _inner

# Vista basada en funciones para el index de administador
@login_required
@superuser_only
def index(request):
    if request.method == "GET":
        return render(request, 'administrador/index.html')
    elif request.method == "POST":
        return HttpResponseForbidden()

# Vistas basadas en funciones

# Función para listar las órdenes registradas
# @staff_member_required
@login_required
@superuser_only
def lista_ordenes(request):
    # Obtenemos todas las ordenes ordendas por id
    ordenes = Orden.objects.all().order_by('id_orden')
    # Asignamos al contexto para el html el queryset de la tabla Orden
    contexto = {'ordenes': ordenes}
    # Listamos las órdenes
    return render(request, 'administrador/lista_ordenes.html', contexto)


# Función para editar una orden en particular
# @staff_member_required
@login_required
@superuser_only
def editar_orden(request,  pk):
    # Obtenemos la instancia (o registro) con el id de la orden que queremos editar
    orden_a_editar = Orden.objects.get(id_orden=pk)
    # Si es una petición get desplegamos el formulario de actualización
    if request.method == 'GET':
        # Instanciamos el formulario de orden
        form = OrdenForm(instance=orden_a_editar)
    # Si es una petición post entonces guardamos los datos del formulario
    elif request.method == 'POST':
        # validamos el form

        #depreciamos el rapartidor
        #rep = Repartidor.objects.filter(id_repatidor = request.POST['id_repartidor_orden']).first()
        #orden_a_editar.id_repartidor_orden = rep
        est = EstadoOrden.objects.filter(id_estado = request.POST['id_estado_orden']).first()
        orden_a_editar.id_estado_orden =  est

        orden_a_editar.id_platillo_orden.clear()
        precio  = 0
        for id_aux in request.POST.getlist('id_platillo_orden'):
            plat = Platillo.objects.filter(id=id_aux).first()
            precio += plat.precio
            orden_a_editar.id_platillo_orden.add(plat)
        orden_a_editar.precio_orden = precio
        #orden_a_editar.id_platillo_orden.set = request.POST.getlist('id_platillo_orden')
        #Orden.objects.filter(id_orden=orden_a_editar.id_orden).update(id_platillo_orden)

        direccion = Direccion.objects.filter(id_direccion = request.POST.get('direccion_entrega_orden')).first()
        orden_a_editar.direccion_entrega_orden = direccion
        orden_a_editar.save()
        return redirect('administrador:listar_ordenes')
    return render(request, 'administrador/ordenes.html', {'form': form})

# Función para eliminar una orden
# @user_passes_test(lambda u: u.is_superuser)
@login_required
@superuser_only
def eliminar_orden(request,  pk):
    # Obtenemos la instancia con el id recibido
    orden_a_editar = Orden.objects.get(id_orden=pk)
    # Eliminamos el registro en la base  de datos
    if request.method == 'POST':
        orden_a_editar.delete()
        # Redirigimos a la lista de órdenes
        return redirect('administrador:listar_ordenes')
    # Cargamos el html para la confirmación de eliminar la orden
    return render(request, 'administrador/eliminar_orden.html', {'orden': orden_a_editar})
