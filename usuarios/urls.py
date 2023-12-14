"""Users URL configuration."""
# Django
from django.contrib import admin
from django.urls import include, path
from .views import *

# Views
app_name = "usuarios"

from usuarios import views

urlpatterns = [
    path('usuarios', views.Index.as_view(), name='usuarios'),

]