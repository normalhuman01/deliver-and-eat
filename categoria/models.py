from django.db import models

# Create your models here.


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(unique=True, null=False, max_length=100)

    class Meta:
        db_table = 'categoria'
        verbose_name_plural = "Categorias"

    def __str__(self):
        return '{}'.format(self.nombre_categoria)
