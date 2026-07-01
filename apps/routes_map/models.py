from django.db import models
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
    # Reemplazo temporal de GeoDjango (PostGIS) a Flotantes normales para Windows:
    stop_lat = models.FloatField(help_text="Latitud geográfica")
    stop_lon = models.FloatField(help_text="Longitud geográfica")

    def __str__(self):
        return self.stop_name

class TrazadoRuta(models.Model):
    """
    Guarda los puntos finos de las calles para dibujar las curvas en el mapa (shapes.txt).
    Como no tenemos LineStringField activo, usamos texto largo para meter un JSON de coordenadas.
    """
    shape_id = models.CharField(max_length=50, primary_key=True)
    coordenadas_json = models.TextField(help_text="Lista de latitudes y longitudes en formato JSON string")

    def __str__(self):
        return f"Trazado {self.shape_id}"