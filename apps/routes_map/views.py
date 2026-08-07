from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Ruta, Parada, TrazadoRuta
from .serializers import RutaSerializer, ParadaSerializer, TrazadoRutaSerializer, RutaGTFSCompletaSerializer, RutaDetalleGTFSSerializer

class RutaViewSet(viewsets.ModelViewSet):
    queryset = Ruta.objects.all()

    def get_serializer_class(self):
        
        if self.action in ['retrieve', 'update', 'partial_update']:
            return RutaDetalleGTFSSerializer
        return RutaSerializer

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
    
    def update(self, request, pk=None):
      print("Entró al update del ViewSet")

      ruta = Ruta.objects.get(pk=pk)

      serializer = RutaGTFSCompletaSerializer(
          ruta,
          data=request.data
      )

      print(serializer.is_valid())

      if not serializer.is_valid():
          print(serializer.errors)
          return Response(serializer.errors, status=400)

      print("Va a ejecutar save()")

      resultado = serializer.save()

      print("Terminó save()")

      return Response({"status": "success", "data": resultado})

      
@api_view(['GET'])
def detalle_ruta_gtfs_view(request, id_ruta):
    try:
        ruta = Ruta.objects.get(pk=id_ruta)
        serializer = RutaDetalleGTFSSerializer(ruta)
        return Response({
            "status": "success",
            "data": serializer.data
        })
    except Ruta.DoesNotExist:
        return Response({"status": "error", "mensaje": "Ruta no encontrada"}, status=404)