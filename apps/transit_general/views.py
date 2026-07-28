from rest_framework import viewsets
from .models import Agencia, Calendario, TarifaAtributo, TarifaRegla
from .serializers import (
    AgenciaSerializer, 
    CalendarioSerializer, 
    TarifaAtributoSerializer, 
    TarifaReglaSerializer
)

class AgenciaViewSet(viewsets.ModelViewSet):
    queryset = Agencia.objects.all()
    serializer_class = AgenciaSerializer

class CalendarioViewSet(viewsets.ModelViewSet):
    queryset = Calendario.objects.all()
    serializer_class = CalendarioSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtro para consultar calendarios según el día de la semana
        dia = self.request.query_params.get('dia', None)
        if dia in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            filter_kwargs = {dia: True}
            queryset = queryset.filter(**filter_kwargs)
        return queryset

class TarifaAtributoViewSet(viewsets.ModelViewSet):
    queryset = TarifaAtributo.objects.all()
    serializer_class = TarifaAtributoSerializer

class TarifaReglaViewSet(viewsets.ModelViewSet):
    queryset = TarifaRegla.objects.all().select_related('fare', 'route')
    serializer_class = TarifaReglaSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        route_id = self.request.query_params.get('ruta', None)
        if route_id is not None:
            queryset = queryset.filter(route_id=route_id)
        return queryset