from rest_framework import serializers
from .models import Agencia, Calendario, TarifaAtributo, TarifaRegla

class AgenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agencia
        fields = '__all__'

class CalendarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendario
        fields = '__all__'

class TarifaAtributoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TarifaAtributo
        fields = '__all__'

class TarifaReglaSerializer(serializers.ModelSerializer):
    
    tarifa_detalle = TarifaAtributoSerializer(source='fare', read_only=True)

    class Meta:
        model = TarifaRegla
        fields = '__all__'