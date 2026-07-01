from rest_framework import serializers
from .models import Agencia, Calendario, TarifaAtributo, TarifaRegla


class AgenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agencia
        fields = '__all__' # Trae todos los campos (agency_id, name, url, timezone)

class CalendarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendario
        fields = '__all__'
        
# apps/transit_general/serializers.py (Agrega esto al final)
 
class TarifaAtributoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TarifaAtributo
        fields = '__all__'

class TarifaReglaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TarifaRegla
        fields = '__all__'