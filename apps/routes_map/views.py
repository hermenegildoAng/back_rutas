from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Ruta, Parada, TrazadoRuta
from .serializers import RutaSerializer, ParadaSerializer, TrazadoRutaSerializer, RutaGTFSCompletaSerializer

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


class RutaGTFSViewSet(viewsets.ViewSet):
    """
    ViewSet personalizado para manejar la creación orquestada de una Ruta GTFS.
    Endpoint principal: POST /api/rutas-gtfs/
    """

    def create(self, request):
        
        serializer = RutaGTFSCompletaSerializer(data=request.data)
        
       
        if serializer.is_valid():
            
            resultado = serializer.save()
            
           
            return Response(
                {
                    "status": "success",
                    "data": resultado
                }, 
                status=status.HTTP_201_CREATED
            )
        
      
        return Response(
            {
                "status": "error",
                "errores": serializer.errors
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )