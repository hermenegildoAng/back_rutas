# usuarios/urls.py
from django.urls import path
from .views import LoginView, RegistroView, PerfilView, CambiarPasswordView, recuperar_password_view

urlpatterns = [
    path('login/', LoginView.as_view(), name='auth_login'),
    path('registro/', RegistroView.as_view(), name='auth_registro'),
    path('perfil/', PerfilView.as_view(), name='auth_perfil'),
    path('cambiar-password/', CambiarPasswordView.as_view(), name='auth_cambiar_password'),
    path('recuperar-password/', recuperar_password_view, name='auth_recuperar_password'),
]