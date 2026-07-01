from rest_framework import serializers
from .models import Viaje, TiempoParada

class ViajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viaje
        fields = '__all__'

class TiempoParadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiempoParada
        fields = '__all__'