from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RutaViewSet, ParadaViewSet, TrazadoRutaViewSet

router = DefaultRouter()
router.register(r'rutas', RutaViewSet)
router.register(r'paradas', ParadaViewSet)
router.register(r'trazados', TrazadoRutaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]