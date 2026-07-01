from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AgenciaViewSet, CalendarioViewSet, TarifaAtributoViewSet, TarifaReglaViewSet

# El router genera automáticamente las rutas de un CRUD estándar
router = DefaultRouter()
router.register(r'agencias', AgenciaViewSet)
router.register(r'calendarios', CalendarioViewSet)
router.register(r'tarifas', TarifaAtributoViewSet)      
router.register(r'tarifas-reglas', TarifaReglaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]