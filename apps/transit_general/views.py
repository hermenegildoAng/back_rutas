from rest_framework import viewsets
from .models import Agencia, Calendario, TarifaAtributo, TarifaRegla
from .serializers import AgenciaSerializer, CalendarioSerializer, TarifaAtributoSerializer, TarifaReglaSerializer

class AgenciaViewSet(viewsets.ModelViewSet):
    queryset = Agencia.objects.all()
    serializer_class = AgenciaSerializer

class CalendarioViewSet(viewsets.ModelViewSet):
    queryset = Calendario.objects.all()
    serializer_class = CalendarioSerializer
    
# apps/transit_general/views.py (Agrega esto al final)
class TarifaAtributoViewSet(viewsets.ModelViewSet):
    queryset = TarifaAtributo.objects.all()
    serializer_class = TarifaAtributoSerializer

class TarifaReglaViewSet(viewsets.ModelViewSet):
    queryset = TarifaRegla.objects.all()
    serializer_class = TarifaReglaSerializer