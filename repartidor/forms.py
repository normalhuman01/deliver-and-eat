"""Formularios Repartidor"""
#Django
from .models import *
from django import forms
from django.forms.widgets import *
from django.contrib.auth.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class FormularioRegistroRepartidor(UserCreationForm):
    """Formulario para registrar un repartidor"""
    nombre = forms.CharField(max_length=64)
    paterno = forms.CharField(max_length=100)
    materno = forms.CharField(max_length=100)
    field_order = ['nombre', 'paterno', 'materno', 'email']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        self.fields['materno'].required = False;
        self.fields['password1'].widget = forms.HiddenInput()
        self.fields['password2'].widget = forms.HiddenInput()

        self.fields['nombre'].widget = TextInput(attrs={
            'id': 'id_nombre',
            'class': 'input-repartidor',
            'name': 'nombre',
            'placeholder': 'Nombre'})

        self.fields['paterno'].widget = TextInput(attrs={
            'id': 'id_paterno',
            'class': 'input-repartidor',
            'name': 'paterno',
            'placeholder': 'Apellido paterno'})

        self.fields['materno'].widget = TextInput(attrs={
            'id': 'id_materno',
            'class': 'input-repartidor',
            'name': 'materno',
            'placeholder': 'Apellido materno'})

        self.fields['email'].widget = TextInput(attrs={
            'id': 'id_email',
            'class': 'input-repartidor',
            'name': 'email',
            'placeholder': 'Correo'})

    class Meta:
        model = User
        fields = ('email',)

    def save(self, commit=True):
        username = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('nombre')
        last_name = self.cleaned_data.get('paterno')
        email = self.cleaned_data.get('email')
        password = User.objects.make_random_password(length=10)
        print(password)

        user = User.objects.create_user(username=email, first_name=first_name, last_name=last_name, email=email, password=password)

        if commit:
            #user.save()
            #return user
            pass
        data = {'user' : user, 'cont' : password}
        return data

    def clean_email(self):
        """Valida que el correo no exista en la base de datos"""
        data = self.cleaned_data.get('email')
        if User.objects.filter(email=data).count() > 0:
            raise forms.ValidationError("Este correo ya existe para un repartidor")

        return data