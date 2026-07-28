from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Ruta, Parada, TrazadoRuta

class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = '__all__'

class ParadaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Parada
        geo_field = 'location'  
        fields = '__all__'

class TrazadoRutaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = TrazadoRuta
        geo_field = 'geometria' 
        fields = '__all__'