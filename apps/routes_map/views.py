from rest_framework import viewsets
from .models import Ruta, Parada, TrazadoRuta
from .serializers import RutaSerializer, ParadaSerializer, TrazadoRutaSerializer

class RutaViewSet(viewsets.ModelViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer

class ParadaViewSet(viewsets.ModelViewSet):
    queryset = Parada.objects.all()
    serializer_class = ParadaSerializer

    def get_queryset(self):
        queryset = Parada.objects.all()
        ruta_id = self.request.query_params.get('ruta', None)
        if ruta_id is not None:
            queryset = queryset.filter(ruta_id=ruta_id)
        return queryset

class TrazadoRutaViewSet(viewsets.ModelViewSet):
    queryset = TrazadoRuta.objects.all()
    serializer_class = TrazadoRutaSerializer

    def get_queryset(self):
        queryset = TrazadoRuta.objects.all()
        ruta_id = self.request.query_params.get('ruta', None)
        if ruta_id is not None:
            queryset = queryset.filter(ruta_id=ruta_id)
        return queryset