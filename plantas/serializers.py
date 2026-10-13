from rest_framework import serializers
from .models import Planta

class PlantaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planta
        fields = '__all__'

    def validate_nombre(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return value

    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a 0.")
        if value >= 1000000:
            raise serializers.ValidationError("El precio no puede superar $1.000.000.")
        return value

    def validate_stock(self, value):
        if value > 9999:
            raise serializers.ValidationError("El stock no puede superar las 9.999 unidades.")
        return value