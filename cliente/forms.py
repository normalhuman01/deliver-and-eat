from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.widgets import *

# Formulario para registro de clientes en la aplicación


class ClienteRegistroForm(UserCreationForm):

    nombre = forms.CharField(max_length=64)
    paterno = forms.CharField(max_length=100)
    materno = forms.CharField(max_length=100)
    telefono = forms.CharField(max_length=10)
    # Ordenamos los campos del formulario
    field_order = ['nombre', 'paterno', 'materno',
                   'telefono', 'email', 'password1', 'password2']
    # Heredamso el modelo User y jalamos determinados atributos

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', )

    # Sobreescribimos el método save para crear una instancia de usuario previamente a la de cliente
    # La jerarquía consiste en todo cliente es un usuario pero un usuario puede no ser un cliente
    def save(self, commit=True):
        # Guardamos el usuario con los datos obtenidos  del form
        username = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('nombre')
        last_name = self.cleaned_data.get('paterno')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')
        user = User.objects.create_user(username=email, first_name=first_name, last_name=last_name,
                                        email=email, password=password)
        if commit:
            pass
        return user

    def clean_email(self):
        """Valida que el correo no exista en la base de datos"""
        data = self.cleaned_data.get('email')
        if User.objects.filter(email=data).count() > 0:
            raise forms.ValidationError("Este correo ya está registrado")
        return data

    def __init__(self, *args, **kwargs):
        super(ClienteRegistroForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget = TextInput(attrs={
            'id': 'id_nombre',
            'class': 'input100',
            'name': 'nombre',
            'placeholder': 'Nombre'})
        self.fields['paterno'].widget = TextInput(attrs={
            'id': 'id_paterno',
            'class': 'input100',
            'name': 'paterno',
            'placeholder': 'Paterno'})
        self.fields['materno'].widget = TextInput(attrs={
            'id': 'id_materno',
            'class': 'input100',
            'name': 'materno',
            'placeholder': 'Materno'})
        self.fields['telefono'].widget = TextInput(attrs={
            'id': 'id_telefono',
            'class': 'input100',
            'name': 'telefono',
            'placeholder': 'Telefono',
            'pattern' : '[0-9]+',
            'title' : 'Ingresa un número telefónico válido'})
        self.fields['email'].widget = TextInput(attrs={
            'id': 'id_email',
            'class': 'input100',
            'name': 'email',
            'placeholder': 'Correo'})
        self.fields['password1'].widget = TextInput(attrs={
            'id': 'id_password1',
            'type': "password",
            'class': 'input100',
            'name': 'password1',
            'placeholder': 'Contraseña'})
        self.fields['password2'].widget = TextInput(attrs={
            'id': 'id_password2',
            'type': "password",
            'class': 'input100',
            'name': 'password2',
            'placeholder': 'Confirmar contraseña'})


# Form para validar inicios de sesión
# Heredamos del form de autenticación de django AuthenticationForm no es
# necesario cargar los campos usaurio contraseña.
# Previamente se definió que el correo es el username
class InicioSesionForm(AuthenticationForm):
    # Validamos los datos recibidos
    def clean(self):

        usuario = self.data["username"]
        clave = self.data["password"]
        # Si el correo no existe en la tabla usuarios mandamos un error de registro
        if (User.objects.filter(username=usuario).count() == 0):
            self.add_error(
                "username", forms.ValidationError("Éste correo no existe")
            )
        # Validamos el correo y contraseña
        user = authenticate(username=usuario, password=clave)
        if user is None:
            self.add_error("password", forms.ValidationError(
                "Contraseña inválida"))

    def __init__(self, *args, **kwargs):
        super(InicioSesionForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = TextInput(attrs={
            'id': 'id_username',
            'class': 'input100',
            'name': 'username',
            'placeholder': 'Correo'})
        self.fields['password'].widget = TextInput(attrs={
            'id': 'id_password',
            'class': 'input100',
            'type': "password",
            'name': 'password',
            'placeholder': 'Contraseña'})


class AgregarDireccion(forms.ModelForm):
    """Formulario para agregar una direccion"""
    descripcion_direccion = forms.CharField(
        label="direccion", max_length=200, required=True)
    id_cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.filter(user_cliente=1))

    class Meta:
        db_table = "direccion"
        model = Direccion
        fields = ("descripcion_direccion", "id_cliente")

    def __init__(self, user, *args, **kwargs):
        super(AgregarDireccion, self).__init__(*args, **kwargs)
        self.fields['id_cliente'].queryset = Cliente.objects.filter(
            user_cliente=user)
