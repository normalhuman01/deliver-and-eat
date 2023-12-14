from django.db import models
#from cliente.models import *
from cliente import models 
from repartidor  import models 
from platillo import  models  
from repartidor.models import *
from cliente.models import * 

# Create your models here.



'''
Modelo Orden, el mapeo correspondiente a las órdenes que generará el usuario en la siguiente
iteración, de momento se tiene para poder simular el cambio de estado de la orden 
como repartidor o administrador
'''

class Orden(models.Model):
	id_orden = models.AutoField(primary_key=True)
	precio_orden = models.IntegerField(null=False, default = 0)
	id_cliente_orden = models.ForeignKey('cliente.Cliente', on_delete=models.SET_DEFAULT, default=0)
	id_repartidor_orden = models.ForeignKey('repartidor.Repartidor',on_delete= models.SET_NULL, blank =True,  null=True)
	id_platillo_orden  = models.ManyToManyField('platillo.Platillo', null=True)
	id_estado_orden =    models.ForeignKey('EstadoOrden',  on_delete=models.SET_DEFAULT, default=0)
	direccion_entrega_orden  = models.ForeignKey('cliente.Direccion', null=True, on_delete=models.CASCADE)
	#Definimos el nombre de la tabla  y el nombre plural para el panel de administrador
	class Meta:
		db_table = 'orden'
		verbose_name_plural = "Ordenes"
'''
La tabla EstadoOrden surge de la necesitadad de tener un catálogo con los estados
posibles para cada orden
1-Pedido realizado
2-Pedido confirmado
3-Pedido listo para recolección
4-Pedido recolectado
5-Pedido entregado
'''
class EstadoOrden(models.Model):
	"""docstring for EstadoOrden"""
	id_estado = models.IntegerField(primary_key=True)
	descripcion_estado = models.CharField(max_length=30)
	#Definimos el nombre de la tabla y plural para cada el panel de administrador
	class Meta:
		db_table = 'estado_orden'
		verbose_name_plural = "EstadosOrden"
	def __str__(self):
		return '{}'.format(self.descripcion_estado)