# usuarios/models.py
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
    
   
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} ({self.get_tipo_usuario_display()})"