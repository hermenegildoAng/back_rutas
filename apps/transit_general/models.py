from django.db import models

class Agencia(models.Model):
    agency_id = models.CharField(max_length=50, primary_key=True, help_text="ID único de la empresa de transporte")
    agency_name = models.CharField(max_length=100)
    agency_url = models.URLField()
    agency_timezone = models.CharField(max_length=50, default="America/Mexico_City")

    def __str__(self):
        return self.agency_name

class Calendario(models.Model):
    service_id = models.CharField(max_length=50, primary_key=True, help_text="ID del bloque de días (Ej: LUN-VIE)")
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
        return self.service_id
    
    
class TarifaAtributo(models.Model):
    fare_id = models.CharField(max_length=50, primary_key=True)
    price = models.DecimalField(max_digits=6, decimal_places=2) # Ej: 10.00
    currency_type = models.CharField(max_length=3, default="MXN")
    payment_method = models.IntegerField(default=0) # 0 = Pago a bordo
    transfers = models.IntegerField(default=0) # 0 = No permite transbordos

class TarifaRegla(models.Model):
    fare = models.ForeignKey(TarifaAtributo, on_delete=models.CASCADE)
    route = models.ForeignKey('routes_map.Ruta', on_delete=models.CASCADE) # Conecta con tus rutas