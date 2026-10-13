from django import forms
from .models import Planta

class PlantaForm(forms.ModelForm):
    class Meta:
        model = Planta
        fields = '__all__'


    def clean_nombre(self):
        inputNombre = self.cleaned_data.get('nombre')
        if len(inputNombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return inputNombre


    def clean_precio(self):
        inputPrecio = self.cleaned_data.get('precio')
        if inputPrecio is not None and inputPrecio <= 0:
            raise forms.ValidationError("El precio debe ser mayor a 0.")
        if inputPrecio is not None and inputPrecio >= 1000000:
            raise forms.ValidationError("El precio no puede superar $1.000.000.")
        return inputPrecio


    def clean_stock(self):
        inputStock = self.cleaned_data.get('stock')
        if inputStock is not None and inputStock > 9999:
            raise forms.ValidationError("El stock debe estar entre 0 y 9.999 unidades.")
        return inputStock