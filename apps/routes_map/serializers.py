from rest_framework import serializers
from .models import Ruta, Parada, TrazadoRuta

class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = '__all__'

class ParadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parada
        fields = '__all__'

class TrazadoRutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrazadoRuta
        fields = '__all__'