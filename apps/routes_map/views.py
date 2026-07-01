from rest_framework import viewsets
from .models import Ruta, Parada, TrazadoRuta
from .serializers import RutaSerializer, ParadaSerializer, TrazadoRutaSerializer

class RutaViewSet(viewsets.ModelViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer

class ParadaViewSet(viewsets.ModelViewSet):
    queryset = Parada.objects.all()
    serializer_class = ParadaSerializer

class TrazadoRutaViewSet(viewsets.ModelViewSet):
    queryset = TrazadoRuta.objects.all()
    serializer_class = TrazadoRutaSerializer