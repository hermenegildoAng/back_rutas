from rest_framework import serializers
from .models import Viaje, TiempoParada

class TiempoParadaSerializer(serializers.ModelSerializer):
    
    parada_nombre = serializers.ReadOnlyField(source='parada.stop_name', default=None)

    class Meta:
        model = TiempoParada
        fields = '__all__'

class ViajeSerializer(serializers.ModelSerializer):
   
    tiempos_parada = TiempoParadaSerializer(many=True, read_only=True, source='tiempoparada_set')

    class Meta:
        model = Viaje
        fields = '__all__'