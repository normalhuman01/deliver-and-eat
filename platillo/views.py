# Django
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User

# Modelos
from .models import Platillo

# Formularios
from .forms import FormularioCrearPlatillo, FormularioSeleccionPlatillo, FormularioEditarPlatillo

# Vistas


class Index(View):
    """Pagina Index para los platillos"""
    template = "platillo/index_platillos.html"

    def get(self, request):
        """Metodo Get"""
        return render(request, self.template)


class CrearPlatillo(View):
    """Pagina para crear un nuevo platillo"""

    template = "platillo/crear_platillo.html"

    def get(self, request):
        formulario = FormularioCrearPlatillo()
        contexto = {"formulario": formulario}
        return render(request, self.template, contexto)

    def post(self, request):
        formulario = FormularioCrearPlatillo(request.POST, request.FILES)
        if formulario.is_valid():
            nombre = formulario.cleaned_data["nombre"]
            descripcion = formulario.cleaned_data["descripcion"]
            precio = formulario.cleaned_data["precio"]
            imagen = formulario.cleaned_data["imagen"]
            formulario.save()
            return redirect("platillos")
        contexto = {"formulario": formulario}
        return render(request, self.template, contexto)


class SeleccionarPlatillo(View):
    """Pagina para seleccionar un platillo existente"""

    template = "platillo/seleccionar.html"

    def get(self, request):
        formulario = FormularioSeleccionPlatillo()
        contexto = {"formulario": formulario}
        return render(request, self.template, contexto)

    def post(self, request):
        formulario = FormularioSeleccionPlatillo(request.POST)
        if formulario.is_valid():
            id_platillo = formulario.cleaned_data["seleccion"].id
            request.session['id'] = id_platillo
            # Esto te redirecciona segun el boton pulsado
            if 'editar' in request.POST:
                return redirect('editar')
            if 'eliminar' in request.POST:
                return redirect('eliminar')
        return HttpResponse("Error al seleccionar platillo")


class EditarPlatillo(View):
    """Pagina para editar un platillo existente"""

    template = "platillo/editar_platillo.html"

    def get(self, request):
        platillo_original = Platillo.objects.get(pk=request.session.get('id'))
        formulario = FormularioEditarPlatillo(instance=platillo_original)
        contexto = {"formulario": formulario,
                    "platillo_original": platillo_original}
        return render(request, self.template, contexto)

    def post(self, request):
        platillo_original = Platillo.objects.get(pk=request.session.get('id'))
        formulario = FormularioEditarPlatillo(
            request.POST, instance=platillo_original, files=request.FILES)
        if formulario.is_valid():
            nombre = formulario.cleaned_data["nombre"]
            descripcion = formulario.cleaned_data["descripcion"]
            precio = formulario.cleaned_data["precio"]
            imagen = formulario.cleaned_data["imagen"]
            platillo_original.nombre = nombre
            platillo_original.descripcion = descripcion
            platillo_original.precio = precio
            platillo_original.imagen = imagen
            formulario.save()
            return redirect('platillos')
        return HttpResponse("Error al editar platillo, intentelo nuevamente")
        contexto = {"formulario": formulario}
        return render(request, self.template, contexto)


class EliminarPlatillo(View):
    """ Vista para eliminar el platillo """

    template = "platillo/eliminar_platillo.html"

    def get(self, request):
        platillo_original = Platillo.objects.get(pk=request.session.get('id'))
        contexto = {"platillo_original": platillo_original}
        return render(request, self.template, contexto)

    def post(self, request):
        platillo_original = Platillo.objects.get(pk=request.session.get('id'))
        platillo_original.delete()
        return redirect('platillos')


class VerPlatillos(View):
    """Vista para ver un listado de todos los platillos"""

    template = "platillo/ver_platillos.html"

    def get(self, request):
        platillos = Platillo.objects.all()
        contexto = {"platillos": platillos}
        return render(request, self.template, contexto)

