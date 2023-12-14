""" Formularios para platillos """

from django import forms
from .models import Platillo, Categoria
from django.contrib.auth.models import User
from django.forms.widgets import FileInput


class FormularioCrearPlatillo(forms.ModelForm):
    """Formulario para crear un nuevo platillo"""
    nombre = forms.CharField(label="nombre", max_length=250, required=True, widget=forms.TextInput(
        attrs={'class': 'campo', 'name': 'nombre'}))
    descripcion = forms.CharField(label="descripcion", max_length=500, required=False, widget=forms.Textarea(
        attrs={'class': 'campoDescripcion', 'name': 'descripcion'}))
    precio = forms.FloatField(label="precio", required=True, widget=forms.NumberInput(
        attrs={'class': 'campo', 'name': 'precio'}))
    imagen = forms.FileField(label="imagen", required=True)
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(
    ), empty_label="Selecciona la categoria")

    class Meta:
        db_table = "platillo"
        model = Platillo
        fields = ("nombre", "descripcion", "precio", "imagen", "categoria")

    def nombre_existente(self):
        """ Metodo para evitar nombres duplicados """
        nombre = self.clean_data["nombre"]
        if Platillo.objects.filter(nombre=nombre).count() > 0:
            raise forms.ValidationError("El nombre del platillo ya existe!")
        return nombre


class FormularioSeleccionPlatillo(forms.ModelForm):
    """Formulario para la seleccion del platillo"""
    seleccion = forms.ModelChoiceField(queryset=Platillo.objects.all())

    class Meta:
        db_table = "platillo"
        model = Platillo
        fields = ("seleccion",)


class FormularioEditarPlatillo(forms.ModelForm):
    """Formulario para editar un platillo"""
    nombre = forms.CharField(label="nombre", max_length=250, required=True, widget=forms.TextInput(
        attrs={'class': 'campo', 'name': 'nombre'}))
    descripcion = forms.CharField(label="descripcion", max_length=500, required=False, widget=forms.Textarea(
        attrs={'class': 'campoDescripcion', 'name': 'descripcion'}))
    precio = forms.FloatField(label="precio", required=True, widget=forms.NumberInput(
        attrs={'class': 'campo', 'name': 'precio'}))
    imagen = forms.FileField(label="imagen", required=True, widget=FileInput)

    class Meta:
        db_table = "platillo"
        model = Platillo
        fields = ("nombre", "descripcion", "precio", "imagen")

    def nombre_existente(self):
        """ Metodo para evitar nombres duplicados """
        nombre = self.clean_data["nombre"]
        if Platillo.objects.filter(nombre=nombre).count() > 0:
            raise forms.ValidationError("El nombre del platillo ya existe!")
        return nombre
