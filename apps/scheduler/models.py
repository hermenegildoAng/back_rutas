from django.db import models
from apps.routes_map.models import Ruta, Parada
from apps.transit_general.models import Calendario

class Viaje(models.Model):
    trip_id = models.CharField(max_length=100, primary_key=True)
    route = models.ForeignKey(Ruta, on_delete=models.CASCADE, related_name="viajes")
    service = models.ForeignKey(Calendario, on_delete=models.CASCADE, related_name="viajes")
    direction_id = models.IntegerField(default=0, choices=[(0, "Ida"), (1, "Vuelta")])

    def __str__(self):
        return f"Viaje {self.trip_id} ({self.route.route_short_name})"

class TiempoParada(models.Model):
    # Aquí dejamos que Django cree su ID numérico automático para control interno
    trip = models.ForeignKey(Viaje, on_delete=models.CASCADE, related_name="tiempos_parada")
    stop = models.ForeignKey(Parada, on_delete=models.CASCADE, related_name="tiempos_parada")
    arrival_time = models.TimeField(help_text="Hora de llegada (HH:MM:SS)")
    departure_time = models.TimeField(help_text="Hora de salida (HH:MM:SS)")
    stop_sequence = models.IntegerField(help_text="Orden de la parada en este viaje (1, 2, 3...)")

    class Meta:
        # Evita que se repita la misma secuencia en un mismo viaje
        unique_together = ("trip", "stop_sequence")

    def __str__(self):
        return f"{self.trip_id} - Sec: {self.stop_sequence} - {self.stop.stop_name}"