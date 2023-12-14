from django.db import models
from categoria import models
from categoria.models import *

# Create your models here.


def directorio_imagen(instance, filename):
    """Obtiene el directorio para guardar las imagenes de los platillos"""

    # Obtenemos la extension del archivo para guardar la imagen solo con el id y nombre del platillo
    extension = filename.rsplit('.', 1)[1]
    return f"platillo/imagen/{instance.id}_{instance.nombre}.{extension}"


class Platillo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.CharField(max_length=500, null=True)
    precio = models.FloatField(null=False, default=0)
    imagen = models.ImageField(null=False, upload_to=directorio_imagen)
    categoria = models.ForeignKey(
        'categoria.Categoria', on_delete=models.CASCADE)

    def __str__(self):
        """Obtiene el nombre del platillo"""
        return self.nombre

    def __repr__(self):
        """Obtiene la representacion en cadena del platillo"""
        return self.__str__()

    def save(self, *args, **kwargs):
        """Sobrecargamos el metodo save para que almacende de forma corrercta las imagenes"""
        if self.pk is None:
            imagen_respaldo = self.imagen
            self.imagen = None
            super(Platillo, self).save(*args, **kwargs)
            self.imagen = imagen_respaldo
        super(Platillo, self).save(*args, **kwargs)

    class Meta:
        db_table = 'platillo'
        verbose_name_plural = "Platillos"

    def get_imagen_path(self):
        """Obtenemos la direccion de la imagen"""
        return f"media/{self.imagen.name}"
