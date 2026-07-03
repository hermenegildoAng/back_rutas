# usuarios/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

UsuarioActual = get_user_model()

# 1. Serializador para ver y editar el perfil
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioActual
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'tipo_usuario']
        # El tipo de usuario no debería poder cambiárselo cualquiera a sí mismo
        read_only_fields = ['tipo_usuario']

# 2. Serializador para Registro de nuevos usuarios
class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UsuarioActual
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'tipo_usuario']

    def create(self, validated_data):
        # Usamos create_user para que encripte la contraseña automáticamente
        user = UsuarioActual.objects.create_user(**validated_data)
        return user

# 3. Serializador para cambiar contraseña (Edición de seguridad)
class CambiarPasswordSerializer(serializers.Serializer):
    password_actual = serializers.CharField(required=True)
    password_nueva = serializers.CharField(required=True, min_length=8)
    password_confirmar = serializers.CharField(required=True)

    def validate(self, data):
        if data['password_nueva'] != data['password_confirmar']:
            raise serializers.ValidationError({"password_nueva": "Las nuevas contraseñas no coinciden."})
        return data