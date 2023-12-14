
from django import forms
from django.contrib.auth.models import User
from .models import *
# Formulario para crear las categorías


class CategoriaForm(forms.ModelForm):
    nombre_categoria = forms.CharField(
        required=True,  max_length=100, label='Nombre Categoria'),

    class Meta:
        model = Categoria
        fields = [
            'nombre_categoria',
        ]

    def clean_nombre_categoria(self):
        data = self.cleaned_data.get('nombre_categoria')
        print("esto es data " + data)
        if Categoria.objects.filter(nombre_categoria=data).count() > 0:
            raise forms.ValidationError("Esta categoría ya existe")
        return data


class FormularioSeleccionCategoria(forms.ModelForm):
    """Formulario para la seleccion de una categoria"""
    seleccion = forms.ModelChoiceField(queryset=Categoria.objects.all())

    class Meta:
        model = Categoria
        fields = ("seleccion",)


class FormularioEditarCategoria(forms.ModelForm):
    """Formulario para editar una categoria"""
    nombre_categoria = forms.CharField(required=True,  max_length=100, label='Nombre Categoria', widget=forms.TextInput(
        attrs={'class': 'campo', 'name': 'nombre'}))

    class Meta:
        model = Categoria
        fields = [
            'nombre_categoria',
        ]

    def clean_nombre_categoria(self):
        data = self.cleaned_data.get('nombre_categoria')
        if Categoria.objects.filter(nombre_categoria=data).count() > 0:
            raise forms.ValidationError("Esta categoría ya existe")
        return data
