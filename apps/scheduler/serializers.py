from rest_framework import serializers
from .models import Viaje, TiempoParada
from apps.routes_map.serializers import ParadaSerializer


class TiempoParadaSerializer(serializers.ModelSerializer):
   
    parada_nombre = serializers.ReadOnlyField(source='stop.stop_name', default=None)
    
    
    parada_detalle = ParadaSerializer(source='stop', read_only=True)

    class Meta:
        model = TiempoParada
        fields = '__all__'


class ViajeSerializer(serializers.ModelSerializer):
   
    tiempos_parada = TiempoParadaSerializer(many=True, read_only=True)
    
   
    ruta_nombre = serializers.ReadOnlyField(source='route.route_short_name', default=None)

    class Meta:
        model = Viaje
        fields = '__all__'