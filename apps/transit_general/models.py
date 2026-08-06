from django.db import models


class Agencia(models.Model):
   
    agency_id = models.CharField(max_length=50, primary_key=True, help_text="ID único de la empresa/secretaría")
    agency_name = models.CharField(max_length=100)
    agency_url = models.URLField(default="https://smyt.gob.mx")
    agency_timezone = models.CharField(max_length=50, default="America/Mexico_City")
    agency_lang = models.CharField(max_length=10, default='es', blank=True)
    
    def __str__(self):
        return self.agency_name


class Calendario(models.Model):
    service_id = models.CharField(max_length=100, blank=True, null=True, help_text="Nombre o alias del servicio (Ej: LUN-VIE)")
    monday = models.BooleanField(default=True)
    tuesday = models.BooleanField(default=True)
    wednesday = models.BooleanField(default=True)
    thursday = models.BooleanField(default=True)
    friday = models.BooleanField(default=True)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)
    start_date = models.DateField(help_text="Fecha de inicio del servicio (YYYY-MM-DD)")
    end_date = models.DateField(help_text="Fecha de fin del servicio (YYYY-MM-DD)")

    def __str__(self):
        return f"{self.service_id or 'Calendario'} (#{self.id})"


class Frecuencia(models.Model):
    trip = models.ForeignKey(
        'scheduler.Viaje', 
        on_delete=models.CASCADE, 
        related_name="frecuencias",
        help_text="Viaje asociado a esta frecuencia"
    )
    start_time = models.TimeField(help_text="Hora de inicio del bloque (HH:MM:SS)")
    end_time = models.TimeField(help_text="Hora de fin del bloque (HH:MM:SS)")
    headway_secs = models.IntegerField(help_text="Intervalo entre salidas en segundos")

    def __str__(self):
        mins = self.headway_secs // 60
        return f"Frecuencia #{self.id} Viaje {self.trip_id}: {self.start_time} - {self.end_time} (Cada {mins} min)"


class TarifaAtributo(models.Model):
    fare_id = models.CharField(max_length=50, blank=True, null=True, help_text="ID de tarifa GTFS")
    price = models.DecimalField(max_digits=6, decimal_places=2, default=10.00) 
    currency_type = models.CharField(max_length=3, default="MXN")
    payment_method = models.IntegerField(default=0, help_text="0 = Pago a bordo")
    transfers = models.IntegerField(default=0, help_text="0 = No permite transbordos")

    def __str__(self):
        return f"Tarifa #{self.id} - ${self.price} {self.currency_type}"


class TarifaRegla(models.Model):
    fare = models.ForeignKey(TarifaAtributo, on_delete=models.CASCADE)
    route = models.ForeignKey('routes_map.Ruta', on_delete=models.CASCADE)

    def __str__(self):
        return f"Regla Tarifa #{self.fare_id} en Ruta {self.route.route_short_name}"