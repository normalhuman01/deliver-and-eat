from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .models import Categoria
from .forms import *
# Create your views here.
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required


def superuser_only(function):
    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return _inner

# Vistas basadas en clases


class Index(View):
    def get(self, request):
        return render(request, 'categoria/index.html')

    def post(self, request):
        return HttpResponseForbidden()
# Vistas basadas en funciones
@login_required
@superuser_only
# Función para cargar una categoría
def crear_categoria(request):
    # Si recibimos petición post
    if request.method == 'POST':
        # Instanciamos el form de categoria con los datos enviados
        form = CategoriaForm(request.POST)
        # Validamos el formulario
        if not form.is_valid():
            # Guardamos cambios
            context = {"form": form}
            return render(request, "categoria/crear_categoria.html", context)
        form.save()
        return redirect('administrador:IndexAdministrador')
    # Si recibimos petición get
    elif request.method == 'GET':
        # Instanciamos el formulario de agregar categoria y se lo asignamos al contexto
        form = CategoriaForm()
        context = {"form": form}
        # Cargamos el html para crear categoría
        return render(request, 'categoria/crear_categoria.html', context)


@login_required
# Función para listar las categorías existentes
def lista_categoria(request):
    # Obtenemos el queryset de las categorías ordenadas alfabéticamente
    categorias = Categoria.objects.all().order_by('id_categoria')
    # Asignamos al contexto el queryset
    contexto = {'categorias': categorias}
    # Cargamos el html con la lista de categorías
    return render(request, 'categoria/lista_categorias.html', contexto)


@login_required
def selecciona_categoria(request):
    """Seleccionamos la categoria"""

    template = 'categoria/seleccion_categoria.html'
    template_editar = 'categoria/editar_categoria.html'
    #cargamos las categorias
    if request.method == 'GET':
        formulario = FormularioSeleccionCategoria()
        contexto = {"formulario": formulario}
        return render(request, template, contexto)
    #editamos o eliminamos la categoria
    elif request.method == 'POST':
        formulario = FormularioSeleccionCategoria(request.POST)
        if formulario.is_valid():
            id_categoria = formulario.cleaned_data["seleccion"].id_categoria
            request.session['id_categoria'] = id_categoria
            # Esto te redirecciona segun el boton pulsado
            if 'editar' in request.POST:
                return redirect('categoria:editar_categoria')
            if 'eliminar' in request.POST:
                return redirect('categoria:eliminar_categoria')
    return HttpResponse("Error al seleccionar la categoria")

#función para editar  la categoria

@login_required
def editar_categoria(request):
    template = "categoria/editar_categoria.html"

    if request.method == 'GET':
        categoria_original = Categoria.objects.get(
            pk=request.session.get('id_categoria'))
        formulario = FormularioEditarCategoria(instance=categoria_original)
        contexto = {"formulario": formulario,
                    "categoria_original": categoria_original}
        return render(request, template, contexto)
    if request.method == 'POST':
        categoria_original = Categoria.objects.get(
        pk=request.session.get('id_categoria'))
        formulario = FormularioEditarCategoria(
            request.POST, instance=categoria_original)
        if not formulario.is_valid():
            context = {"formulario": formulario}
            return render(request, 'categoria/editar_categoria.html', context)
        else:
            nombre = formulario.cleaned_data["nombre_categoria"]
            categoria_original.nombre_categoria = nombre
            formulario.save()
            return redirect('categoria:selecciona_categoria')
        

#función para eliminar la categoría
@login_required
def eliminar_categoria(request):
    template = "categoria/eliminar_categoria.html"
    if request.method == 'GET':
        return render(request, template)
    if request.method == 'POST':
        categoria_original = Categoria.objects.get(
            pk=request.session.get('id_categoria'))
        categoria_original.delete()
        return redirect("categoria:selecciona_categoria")
    return HttpResponse("Error al eliminar categoria")
