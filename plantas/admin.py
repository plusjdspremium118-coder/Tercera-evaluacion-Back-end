from django.contrib import admin
from .models import Planta
# Register your models here.

class PlantaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'tipo', 'precio', 'stock']

admin.site.register(Planta, PlantaAdmin)