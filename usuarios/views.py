"""Users views."""
# Django
from django.shortcuts import render, redirect
from django.views import View
from usuarios.forms import  *
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import  * 
from django.contrib.auth import authenticate, login, logout

class Index(View):
    """Pagina Index para los usuarios"""

    template = "usuarios/index.html"

    def get(self, request):
        """Metodo Get"""
        return render(request, self.template)