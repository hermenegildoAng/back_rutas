# apps/scheduler/models.py
from django.db import models
from apps.routes_map.models import Ruta, Parada, TrazadoRuta
from apps.transit_general.models import Calendario


class Viaje(models.Model):
    trip_id = models.CharField(max_length=100, primary_key=True)
    route = models.ForeignKey(Ruta, on_delete=models.CASCADE, related_name="viajes")
    service = models.ForeignKey(Calendario, on_delete=models.CASCADE, related_name="viajes")
    
    
    shape = models.ForeignKey(
        TrazadoRuta, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="viajes",
        help_text="Trazado geoespacial (shape_id) asociado a este viaje"
    )
    
    direction_id = models.IntegerField(
        default=0, 
        choices=[(0, "Ida"), (1, "Vuelta")],
        help_text="0 para Ida, 1 para Vuelta (Estándar GTFS)"
    )

    def __str__(self):
        dir_label = "Ida" if self.direction_id == 0 else "Vuelta"
        return f"Viaje {self.trip_id} - {self.route.route_short_name} ({dir_label})"


class TiempoParada(models.Model):
    trip = models.ForeignKey(Viaje, on_delete=models.CASCADE, related_name="tiempos_parada")
    stop = models.ForeignKey(Parada, on_delete=models.CASCADE, related_name="tiempos_parada")
    
    
    arrival_time = models.TimeField(null=True, blank=True, help_text="Hora de llegada (HH:MM:SS)")
    departure_time = models.TimeField(null=True, blank=True, help_text="Hora de salida (HH:MM:SS)")
    
    stop_sequence = models.PositiveIntegerField(help_text="Orden de la parada en este viaje (1, 2, 3...)")

    class Meta:
        ordering = ['stop_sequence']  
        unique_together = ("trip", "stop_sequence")

    def __str__(self):
        return f"{self.trip.trip_id} - Sec {self.stop_sequence}: {self.stop.stop_name}"