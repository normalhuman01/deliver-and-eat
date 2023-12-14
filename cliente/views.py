from django.shortcuts import render
from django.views import View

# Create your views here.

from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import *
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from repartidor.models import *

from administrador.models import *
# Create your views here.
from django.contrib.auth.decorators import login_required


class RegistroCliente(View):
    """New User Sign Up."""

    def get(self, request):
        """Render sign up form."""
        form = ClienteRegistroForm()
        context = {"form": form}
        return render(request, 'cliente/registro_cliente.html', context)

    def post(self, request):
        form = ClienteRegistroForm(request.POST)
        if not form.is_valid():
            context = {"form": form}
            return render(request, 'cliente/registro_cliente.html', context)
        print("es valido")
        user = form.save(commit=False)
        user.is_active = True
        user.save()

        user2 = Cliente(
            user_cliente=user,
            nombre_cliente=form.cleaned_data["nombre"],
            apellido_pa_cliente=form.cleaned_data["paterno"],
            apellido_ma_cliente=form.cleaned_data["materno"],
            telefono_cliente=form.cleaned_data["telefono"],
        )
        user2.save()
        return redirect("cliente:IndexCliente")
# Función que carga el login


class Index(View):
    def get(self, request):
        form = InicioSesionForm()
        context = {"form": form}
        return render(request, "cliente/index.html", context)

    def post(self, request):
        """Receive and validate sign up form."""
        form = InicioSesionForm(data=request.POST)
        if not form.is_valid():
            print("no es válido")
            context = {"form": form}
            return render(request, "cliente/index.html", context)

        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        # As simple as telling django the user to login.
        login(request, user)
        u = User.objects.get(username=user.username)

        cli = Cliente.objects.filter(user_cliente=u).first()

        rep = Repartidor.objects.filter(user=u).first()
        if(not(cli is None)):
            return redirect('cliente:HomeCliente')
        elif(not(rep is None)):
            return render(request, "repartidor/index.html")
        else:
            if(u.is_superuser):
                return render(request, "administrador/index.html")
            else:
                return render("<h1>asdads</h1>")

# Función para ver el menú de platillos
@login_required
def ver_menu(request):
    platillos = Platillo.objects.all()
    contexto = {"platillos": platillos}
    return render(request, "cliente/ver_menu.html", contexto)


@login_required
def HomeCliente(request):
    if request.method == "GET":
        return render(request, "cliente/home.html")

# Clase para cerrar sesión del usuario


class CerrarSesion(View):
    def get(self, request):
        logout(request)
        return redirect("cliente:IndexCliente")

# Función para cargar el carrito de compras


@login_required
def CarritoView(request):
    if request.method == 'GET':
        user = request.user
        user_1 = User.objects.get(id=user.id)
        print(user_1)
        cliente = Cliente.objects.filter(user_cliente=user_1).first()
        print(cliente)
        
        carrito = Carrito.objects.filter(
            id_cliente_carrito=cliente.id_cliente).all()
        for elem in carrito:
            platillo_activo = Platillo.objects.filter(id=elem.id_platillo_carrito).exists()
            if(platillo_activo == False):
                Carrito.objects.filter(id_platillo_carrito=elem.id_platillo_carrito,id_cliente_carrito=cliente.id_cliente).delete()   
        carrito = Carrito.objects.filter(
            id_cliente_carrito=cliente.id_cliente).all()
        context = {'carrito': carrito}
        return render(request, "cliente/checkout.html", context)

# Función para agregar un platillo al carrito


@login_required
def agregar_al_carrito(request, pk):
    # Obtenemos el usuario
    user = request.user
    user_1 = User.objects.get(id=user.id)
    cliente = Cliente.objects.filter(user_cliente=user_1).first()
    product = Platillo.objects.get(id=pk)
    ya_agregado = Carrito.objects.filter(
        id_platillo_carrito=product.id, id_cliente_carrito=cliente.id_cliente).exists()
    if(ya_agregado == False):
        agregado_carrito = Carrito(id_platillo_carrito=product.id, nombre_platillo_carrito=product.nombre,
                                   id_cliente_carrito=cliente.id_cliente, precio_platillo_carrito=product.precio)
        agregado_carrito.save()
    else:
        pass
    return redirect('cliente:carrito')

# Función para quitar un platillo del carrito


@login_required
def quitar_del_carrito(request, pk):
    # Obtenemos al usuario
    user = request.user
    user_1 = User.objects.get(id=user.id)
    cliente = Cliente.objects.filter(user_cliente=user_1).first()
    product = Platillo.objects.get(id=pk)
    Carrito.objects.filter(id_platillo_carrito=product.id,
                           id_cliente_carrito=cliente.id_cliente).delete()
    return redirect('cliente:carrito')

# Función para confirmar la compra, se requiere por parte del usuario
# que cree y seleccione la dirección de entrega en caso de no existir o simplemente
# seleccione una ya existente
# para generar la orden debemos obtener todos los datos del usuario así como los platillos
# que tiene agregado a su carrito

@login_required
def confirmar(request):
    # Obtenemos el usuario que manda la petición
    user = request.user
    user_1 = User.objects.get(id=user.id)
    cliente = Cliente.objects.filter(user_cliente=user_1).first()
    cliente_id = cliente.id_cliente

    # Usamos get para mostrar las direcciones del usuario
    if request.method == 'GET':
        direcciones = Direccion.objects.filter(id_cliente=cliente)
        formulario = AgregarDireccion(user_1)
        contexto = {"formulario": formulario,
                    "direcciones": direcciones, "cliente": cliente}
        return render(request, "cliente/agregar_seleccionar_direccion.html", contexto)
    # Usamos post para guardar la nueva dirección del cliente
    if request.method == 'POST':
        if 'agregar' in request.POST:
            formulario = AgregarDireccion(user_1, request.POST)
            if formulario.is_valid():
                id_cliente = formulario.cleaned_data["id_cliente"]
                descripcion_direccion = formulario.cleaned_data["descripcion_direccion"]
                formulario.save()
                return redirect('cliente:confirmar')
        if 'seleccion' in request.POST:
            # Aquí ya estamos seleccionando una dirección existente de entrega y generando la orden con el carrito de compras existente
            estado_orden = EstadoOrden.objects.filter(id_estado=1).first()
            direccion_seleccionada = request.POST.get("seleccion", "")
            direccion_final = Direccion.objects.filter(
                id_direccion=direccion_seleccionada).first()
            carrito = Carrito.objects.filter(
                id_cliente_carrito=cliente.id_cliente).all()
            contador_precio = 0
            for elem in carrito:
                platillo_carrito_cliente = Platillo.objects.filter(
                    id=elem.id_platillo_carrito).first()
                contador_precio += platillo_carrito_cliente.precio
            orden_generada = Orden(precio_orden=contador_precio, id_cliente_orden=cliente,
                                   id_estado_orden=estado_orden, direccion_entrega_orden=direccion_final)
            orden_generada.save()
            for elem in carrito:
                platillo_carrito_cliente = Platillo.objects.filter(
                    id=elem.id_platillo_carrito).first()
                orden_generada.id_platillo_orden.add(platillo_carrito_cliente)
            orden_generada.save()
            for elem in carrito:
                Carrito.objects.filter(id_platillo_carrito=elem.id_platillo_carrito,
                                       id_cliente_carrito=elem.id_cliente_carrito).delete()
            x = str(orden_generada.id_orden)
            contexto = {'x': x}
            return render(request, "cliente/confirmacion.html", contexto)

    return HttpResponse("Ocurrio un error interno, intentalo más tarde o agrega una dirección distinta")


# Funcion que permite al cliente visualizar sus historial de órdenes
@login_required
def historial_ordenes(request):
    cliente = Cliente.objects.get(user_cliente=request.user)
    estado = EstadoOrden.objects.get(id_estado=5)
    ordenes = Orden.objects.filter(
        id_cliente_orden=cliente, id_estado_orden=estado).order_by('id_orden')
    contexto = {'ordenes': ordenes}
    return render(request, "cliente/historial_ordenes.html", contexto)

# Funcion que permite al cliente visualizar las ordenes que aún no le han sido entregadas
@login_required
def ordenes_activas(request):
    cliente = Cliente.objects.get(user_cliente=request.user)
    estado = EstadoOrden.objects.get(id_estado=5)
    ordenes = Orden.objects.filter(id_cliente_orden=cliente).exclude(
        id_estado_orden=estado).order_by('id_orden')
    contexto = {'ordenes': ordenes}
    return render(request, "cliente/ordenes_activas.html", contexto)
