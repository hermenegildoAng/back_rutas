# apps/routes_map/models.py
from django.contrib.gis.db import models 
from apps.transit_general.models import Agencia


class Ruta(models.Model):
    route_id = models.CharField(max_length=50, primary_key=True)
    agency = models.ForeignKey(Agencia, on_delete=models.CASCADE, related_name="rutas")
    route_short_name = models.CharField(max_length=20, help_text="Ej: R-10 o Combis UTT")
    route_long_name = models.CharField(max_length=150)
    route_type = models.IntegerField(default=3, help_text="3 significa Autobús/Combi en el estándar GTFS")



    def __str__(self):
        return f"{self.route_short_name} - {self.route_long_name}"


class Parada(models.Model):
    stop_id = models.CharField(max_length=50, primary_key=True)
    stop_name = models.CharField(max_length=150)
    
 
    location = models.PointField(srid=4326, help_text="Ubicación geográfica (Punto en PostGIS)")

    def __str__(self):
        return self.stop_name

class TrazadoRuta(models.Model):
    shape_id = models.CharField(max_length=50, primary_key=True)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE, related_name="trazados", null=True, blank=True)
    
   
    direccion = models.IntegerField(default=0, choices=[(0, 'Ida'), (1, 'Vuelta')])
    
   
    duracion_estimada_min = models.PositiveIntegerField(
        default=30, 
        help_text="Duración total del recorrido en minutos. Sirve para calcular la hora fin en stop_times.txt"
    )
    
   
    geometria = models.LineStringField(srid=4326, help_text="Línea de la ruta (LineString)")

    def __str__(self):
        dir_text = "Ida" if self.direccion == 0 else "Vuelta"
        return f"{self.shape_id} - {self.ruta.route_short_name if self.ruta else ''} ({dir_text})"