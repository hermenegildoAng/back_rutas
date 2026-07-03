# usuarios/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    # Definimos los roles que tendrá tu sistema en la Secretaría
    ROLES_CHOICES = [
        ('admin', 'Administrador'),
        ('capturador', 'Capturista'),
        ('consultor', 'Consultor'),
    ]
    
    # Añadimos tu campo personalizado
    tipo_usuario = models.CharField(
        max_length=20, 
        choices=ROLES_CHOICES, 
        default='capturador',
    )
    
    # Hacemos que el correo sea obligatorio para la recuperación de contraseña
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} ({self.get_tipo_usuario_display()})"