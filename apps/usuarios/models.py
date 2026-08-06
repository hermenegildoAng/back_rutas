from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES_CHOICES = [
        ('admin', 'Administrador'),
        ('capturador', 'Capturista'),
    ]

    
    tipo_usuario = models.CharField(
        max_length=20, 
        choices=ROLES_CHOICES, 
        default='capturador',
    )
    
    
    nombre_completo = models.CharField(
        max_length=150, 
        blank=True, 
        verbose_name="Nombre Completo"
    )

    
    email = models.EmailField(unique=True)

    
    activo = models.BooleanField(
        default=True, 
        help_text="Indica si el usuario tiene acceso al sistema."
    )

    def __str__(self):
        return f"{self.nombre_completo or self.username} ({self.get_tipo_usuario_display()})"