from rest_framework import viewsets
from .models import Viaje, TiempoParada
from .serializers import ViajeSerializer, TiempoParadaSerializer

class ViajeViewSet(viewsets.ModelViewSet):
    queryset = Viaje.objects.all()
    serializer_class = ViajeSerializer

class TiempoParadaViewSet(viewsets.ModelViewSet):
    queryset = TiempoParada.objects.all()
    serializer_class = TiempoParadaSerializer