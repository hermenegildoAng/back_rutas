from rest_framework import viewsets
from .models import Viaje, TiempoParada
from .serializers import ViajeSerializer, TiempoParadaSerializer

class ViajeViewSet(viewsets.ModelViewSet):
    
    queryset = Viaje.objects.all().prefetch_related('tiempoparada_set')
    serializer_class = ViajeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        ruta_id = self.request.query_params.get('ruta', None)
        service_id = self.request.query_params.get('service_id', None)
        
        if ruta_id is not None:
            queryset = queryset.filter(ruta_id=ruta_id)
        if service_id is not None:
            queryset = queryset.filter(service_id=service_id)
            
        return queryset

class TiempoParadaViewSet(viewsets.ModelViewSet):
    queryset = TiempoParada.objects.all().select_related('viaje', 'parada')
    serializer_class = TiempoParadaSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        viaje_id = self.request.query_params.get('viaje', None)
        
        if viaje_id is not None:
           
            queryset = queryset.filter(viaje_id=viaje_id).order_by('stop_sequence')
            
        return queryset