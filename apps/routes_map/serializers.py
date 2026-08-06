from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Ruta, Parada, TrazadoRuta
from django.db import transaction
from django.contrib.gis.geos import Point, GEOSGeometry
import json
from datetime import datetime, timedelta
from apps.transit_general.models import Agencia, Calendario, Frecuencia
from apps.routes_map.models import Ruta, Parada, TrazadoRuta
from apps.scheduler.models import Viaje, TiempoParada


class RutaSerializer(serializers.ModelSerializer):
   
    agencia_nombre = serializers.ReadOnlyField(source='agency.agency_name', default=None)

    class Meta:
        model = Ruta
        fields = '__all__'


class ParadaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Parada
        geo_field = 'location'  
        fields = '__all__'


class TrazadoRutaSerializer(GeoFeatureModelSerializer):
   
    ruta_nombre = serializers.ReadOnlyField(source='ruta.route_short_name', default=None)

    class Meta:
        model = TrazadoRuta
        geo_field = 'geometria' 
        fields = '__all__'



class BloqueHorarioSerializer(serializers.Serializer):
    desde = serializers.TimeField(format='%H:%M')
    hasta = serializers.TimeField(format='%H:%M')
    intervalo = serializers.IntegerField(min_value=1, help_text="Intervalo en minutos")

class CalendarioPayloadSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=100)
    lunes = serializers.BooleanField()
    martes = serializers.BooleanField()
    miercoles = serializers.BooleanField()
    jueves = serializers.BooleanField()
    viernes = serializers.BooleanField()
    sabado = serializers.BooleanField()
    domingo = serializers.BooleanField()
    fecha_inicial = serializers.DateField()
    fecha_final = serializers.DateField()
    bloques = BloqueHorarioSerializer(many=True)

class ParadaPayloadSerializer(serializers.Serializer):
    folio_parada = serializers.CharField(max_length=50, required=False, allow_blank=True)
    nombre_parada = serializers.CharField(max_length=150)
    latitud = serializers.FloatField()
    longitud = serializers.FloatField()
    orden_parada = serializers.IntegerField()

class ViajeRegresoSerializer(serializers.Serializer):
    tiene_viaje_regreso = serializers.BooleanField()
    mismos_horarios = serializers.BooleanField(required=False, default=False)
    mismas_paradas = serializers.BooleanField(required=False, default=False)
    paradas = ParadaPayloadSerializer(many=True, required=False)

# ==========================================
# SERIALIZER PRINCIPAL ORQUESTADOR
# ==========================================
class RutaGTFSCompletaSerializer(serializers.Serializer):
    # Datos de Agencia y Ruta
    agency_id = serializers.CharField(max_length=50) 
    route_id = serializers.CharField(max_length=50, required=False, allow_blank=True)
    route_short_name = serializers.CharField(max_length=20)
    route_long_name = serializers.CharField(max_length=150)
    route_type = serializers.IntegerField()
    duracion_ruta = serializers.IntegerField(min_value=1, help_text="Minutos")
    
    # Datos Espaciales y Relacionales
    geometria_linea = serializers.DictField()
    calendarios = CalendarioPayloadSerializer(many=True)
    paradas = ParadaPayloadSerializer(many=True)
    viaje_regreso = ViajeRegresoSerializer(required=False)

    def create(self, validated_data):
        with transaction.atomic():
            
            # ==========================================
            # 1. AGENCIA Y RUTA
            # ==========================================
            agencia = Agencia.objects.get(agency_id=validated_data['agency_id'])

            ruta = Ruta.objects.create(
                route_id=validated_data.get('route_id'),
                agency=agencia,
                route_short_name=validated_data['route_short_name'],
                route_long_name=validated_data['route_long_name'],
                route_type=validated_data['route_type']
            )

            # ==========================================
            # 2. TRAZADO ÚNICO (SHAPE) Y PARADAS DE IDA
            # ==========================================
            geojson_str = json.dumps(validated_data['geometria_linea'])
            
            # Guardamos un solo trazado que servirá para ambas direcciones
            trazado_base = TrazadoRuta.objects.create(
                shape_id=f"shp_{ruta.id}",
                ruta=ruta,
                direccion=0, # Por defecto lo dejamos en 0, GTFS usará el direction_id del Viaje
                duracion_estimada_min=validated_data['duracion_ruta'],
                geometria=GEOSGeometry(geojson_str)
            )

            paradas_ida_obj = []
            paradas_data_ordenadas = sorted(validated_data['paradas'], key=lambda x: x['orden_parada'])
            
            for p_data in paradas_data_ordenadas:
                punto_geos = Point(p_data['longitud'], p_data['latitud'], srid=4326)
                parada = Parada.objects.create(
                    stop_id=p_data.get('folio_parada'),
                    stop_name=p_data['nombre_parada'],
                    location=punto_geos
                )
                paradas_ida_obj.append(parada)

            # ==========================================
            # 3. PARADAS DE VUELTA (Si aplica)
            # ==========================================
            viaje_regreso_data = validated_data.get('viaje_regreso', {})
            tiene_regreso = viaje_regreso_data.get('tiene_viaje_regreso', False)
            paradas_vuelta_obj = []
            
            if tiene_regreso:
                if viaje_regreso_data.get('mismas_paradas', False):
                    # Solo invertimos el orden lógico de las paradas, sin tocar el trazado
                    paradas_vuelta_obj = list(reversed(paradas_ida_obj))
                else:
                    # Creamos las nuevas paradas exclusivas de regreso
                    paradas_vuelta_data = sorted(viaje_regreso_data.get('paradas', []), key=lambda x: x['orden_parada'])
                    for p_data in paradas_vuelta_data:
                        punto_geos = Point(p_data['longitud'], p_data['latitud'], srid=4326)
                        parada = Parada.objects.create(
                            stop_id=p_data.get('folio_parada'),
                            stop_name=p_data['nombre_parada'],
                            location=punto_geos
                        )
                        paradas_vuelta_obj.append(parada)

            # ==========================================
            # 4. CALENDARIOS, TRIPS, FRECUENCIAS Y STOP_TIMES
            # ==========================================
            tiempo_base = datetime.strptime("00:00:00", "%H:%M:%S")

            for cal_data in validated_data['calendarios']:
                calendario = Calendario.objects.create(
                    service_id=f"srv_{ruta.id}_{cal_data['nombre']}",
                    monday=cal_data['lunes'],
                    tuesday=cal_data['martes'],
                    wednesday=cal_data['miercoles'],
                    thursday=cal_data['jueves'],
                    friday=cal_data['viernes'],
                    saturday=cal_data['sabado'],
                    sunday=cal_data['domingo'],
                    start_date=cal_data['fecha_inicial'],
                    end_date=cal_data['fecha_final']
                )

                # ------------------- PROCESO IDA -------------------
                viaje_ida = Viaje.objects.create(
                    trip_id=f"trp_{ruta.id}_{calendario.id}_ida",
                    route=ruta,
                    service=calendario,
                    shape=trazado_base,  # <- Usamos el trazado único
                    direction_id=0       # <- Aquí marcamos que es Ida
                )

                for bloque in cal_data['bloques']:
                    Frecuencia.objects.create(
                        trip=viaje_ida,
                        start_time=bloque['desde'],
                        end_time=bloque['hasta'],
                        headway_secs=bloque['intervalo'] * 60
                    )

                num_paradas_ida = len(paradas_ida_obj)
                min_entre_paradas_ida = validated_data['duracion_ruta'] / (num_paradas_ida - 1) if num_paradas_ida > 1 else 0

                for idx, parada_obj in enumerate(paradas_ida_obj):
                    mins_acum = min_entre_paradas_ida * idx
                    hora_llegada = (tiempo_base + timedelta(minutes=mins_acum)).time()

                    TiempoParada.objects.create(
                        trip=viaje_ida, stop=parada_obj,
                        arrival_time=hora_llegada, departure_time=hora_llegada,
                        stop_sequence=idx + 1
                    )

                # ------------------- PROCESO VUELTA -------------------
                if tiene_regreso:
                    viaje_vuelta = Viaje.objects.create(
                        trip_id=f"trp_{ruta.id}_{calendario.id}_vuelta",
                        route=ruta,
                        service=calendario,
                        shape=trazado_base,  # <- Reciclamos exactamente el mismo trazado
                        direction_id=1       # <- Aquí marcamos que es Vuelta
                    )

                    num_paradas_vuelta = len(paradas_vuelta_obj)
                    min_entre_paradas_vuelta = validated_data['duracion_ruta'] / (num_paradas_vuelta - 1) if num_paradas_vuelta > 1 else 0

                    for idx, parada_obj in enumerate(paradas_vuelta_obj):
                        mins_acum = min_entre_paradas_vuelta * idx
                        hora_llegada = (tiempo_base + timedelta(minutes=mins_acum)).time()

                        TiempoParada.objects.create(
                            trip=viaje_vuelta, stop=parada_obj,
                            arrival_time=hora_llegada, departure_time=hora_llegada,
                            stop_sequence=idx + 1
                        )
                    
                    for bloque in cal_data['bloques']:
                        Frecuencia.objects.create(
                            trip=viaje_vuelta,
                            start_time=bloque['desde'],
                            end_time=bloque['hasta'],
                            headway_secs=bloque['intervalo'] * 60
                        )

            return {
                "ruta_id": ruta.id,
                "mensaje": "Ruta guardada exitosamente. Trazado único vinculado a viajes de Ida y Vuelta."
            }