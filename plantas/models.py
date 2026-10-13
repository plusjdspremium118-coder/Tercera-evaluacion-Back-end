from django.db import models

# Create your models here.
class Planta(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=80, verbose_name='Nombre')
    tipo = models.CharField(max_length=30, verbose_name='Tipo')
    precio = models.IntegerField(verbose_name='Precio')
    stock = models.PositiveIntegerField(default=0, verbose_name='Stock')
    descripcion = models.TextField(verbose_name='Descripción', null=True, blank=True)
    imagen = models.ImageField(upload_to='imagenes/', verbose_name='Imagen', null=True)

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"


    def delete(self, using=None, keep_parents=False):
        if self.imagen:
            self.imagen.storage.delete(self.imagen.name)
        super().delete()