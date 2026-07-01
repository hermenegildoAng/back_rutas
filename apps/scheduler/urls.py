from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ViajeViewSet, TiempoParadaViewSet

router = DefaultRouter()
router.register(r'viajes', ViajeViewSet)
router.register(r'tiempos-parada', TiempoParadaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]