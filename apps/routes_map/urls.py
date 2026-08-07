from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RutaViewSet, ParadaViewSet, TrazadoRutaViewSet, RutaGTFSViewSet, detalle_ruta_gtfs_view

router = DefaultRouter()
router.register(r'rutas', RutaViewSet)
router.register(r'paradas', ParadaViewSet)
router.register(r'trazados', TrazadoRutaViewSet)

router.register(r'rutas-gtfs', RutaGTFSViewSet, basename='rutas-gtfs') 


urlpatterns = [
    path('', include(router.urls)),
    path('rutas-gtfs/<int:id_ruta>/detalle/', detalle_ruta_gtfs_view, name='detalle-ruta-gtfs'),
]