from django.urls import path, re_path
from . import views
# imports para autenticar el usuario
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

# funcion para autenticar el usuario


def superuser_only(function):
    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return _inner


urlpatterns = [
    # Vistas de clase
    path('', superuser_only(views.Index.as_view()), name='platillos'),
    path('crear',
         superuser_only(views.CrearPlatillo.as_view()), name="crear_platillo"),
    path('seleccionar', superuser_only(views.SeleccionarPlatillo.as_view()),
         name="seleccionar"),
    path('editar',
         superuser_only(views.EditarPlatillo.as_view()), name="editar"),
    path('eliminar', superuser_only(
        views.EliminarPlatillo.as_view()), name="eliminar"),
    #deprecated 
    #path('ver', superuser_only(views.VerPlatillos.as_view()), name="ver"),
    path('ver', views.VerPlatillos.as_view(), name="ver"),

]

