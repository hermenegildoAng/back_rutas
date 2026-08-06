# usuarios/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, get_user_model
from .serializers import UsuarioSerializer, RegistroSerializer, CambiarPasswordSerializer

UsuarioActual = get_user_model()

# 1. Vista de Login (Provisional sin JWT)
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            serializer = UsuarioSerializer(user)
            return Response({
                "msg": "¡Inicio de sesión exitoso!",
                "token_placeholder": "AQUÍ_IRÁ_EL_JWT_DESPUÉS",
                "usuario": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "Credenciales inválidas"}, status=status.HTTP_400_BAD_REQUEST)

# 2. Vista de Registro
class RegistroView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegistroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Usuario registrado exitosamente"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 3. Vista del Perfil (Ver y Editar Datos Básicos)
class PerfilView(APIView):
    # Por ahora AllowAny para que puedas probarla desde el front sin el JWT metido en las cabeceras
    permission_classes = [permissions.AllowAny] 

    def get(self, request):
        # Simulación: Tomamos el primer usuario de la BD temporalmente en lo que hay auth real
        user = request.user if request.user.is_authenticated else UsuarioActual.objects.first()
        if not user:
            return Response({"error": "No hay usuarios en la base de datos"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UsuarioSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user if request.user.is_authenticated else UsuarioActual.objects.first()
        serializer = UsuarioSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Perfil actualizado", "usuario": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 4. Vista para cambiar contraseña
class CambiarPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user = request.user if request.user.is_authenticated else UsuarioActual.objects.first()
        serializer = CambiarPasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            if not user.check_password(serializer.validated_data['password_actual']):
                return Response({"password_actual": "La contraseña actual es incorrecta."}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data['password_nueva'])
            user.save()
            return Response({"msg": "Contraseña actualizada correctamente"}, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 5. Vista de Recuperación de contraseña (Simulación)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def recuperar_password_view(request):
    email = request.data.get('email')
    if not email:
        return Response({"error": "El correo electrónico es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        
    # Comprobar si existe el correo
    existe = UsuarioActual.objects.filter(email=email).exists()
    
    # Por seguridad, es buena práctica responder que "se envió" incluso si no existe,
    # pero para tus pruebas te devuelvo si lo encontró o no.
    if existe:
        return Response({"msg": f"Se ha enviado un enlace de recuperación al correo: {email}"}, status=status.HTTP_200_OK)
    return Response({"error": "No encontramos ningún usuario con ese correo electrónico."}, status=status.HTTP_404_NOT_FOUND)


# 6. MÓDULO ADMINISTRATIVO: Listar todos los usuarios y Registrar uno nuevo
class UsuarioListCreateView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # Devuelve todos los usuarios ordenados por el más reciente
        usuarios = UsuarioActual.objects.all().order_by('-id')
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Usa RegistroSerializer para crear y encriptar la clave temporal automáticamente
        serializer = RegistroSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            # Retornamos los datos completos del usuario con UsuarioSerializer para que el Front los agregue a la lista
            data_response = UsuarioSerializer(usuario).data
            return Response(data_response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 7. MÓDULO ADMINISTRATIVO: Editar/Cambiar estado (Activo/Inactivo) de un usuario específico
class UsuarioDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def patch(self, request, pk):
        try:
            usuario = UsuarioActual.objects.get(pk=pk)
        except UsuarioActual.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Actualización parcial (ideal para cambiar el booleano 'activo')
        serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)