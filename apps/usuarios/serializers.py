from rest_framework import serializers
from django.contrib.auth import get_user_model

UsuarioActual = get_user_model()


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioActual
        fields = ['id', 'username', 'email', 'nombre_completo', 'tipo_usuario', 'activo']
        read_only_fields = ['tipo_usuario', 'username']


class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UsuarioActual
        fields = ['username', 'email', 'password', 'nombre_completo', 'tipo_usuario', 'activo']

    def create(self, validated_data):
        user = UsuarioActual.objects.create_user(**validated_data)
        return user


class CambiarPasswordSerializer(serializers.Serializer):
    password_actual = serializers.CharField(required=True)
    password_nueva = serializers.CharField(required=True, min_length=8)
    password_confirmar = serializers.CharField(required=True)

    def validate(self, data):
        if data['password_nueva'] != data['password_confirmar']:
            raise serializers.ValidationError({"password_nueva": "Las nuevas contraseñas no coinciden."})
        return data