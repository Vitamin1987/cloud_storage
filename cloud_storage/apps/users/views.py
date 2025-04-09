from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from apps.users.serializers import UserSerializer, LoginSerializer, UserProfileSerializer


class RegisterView(APIView):
    """APIView для регистрации пользователя."""
    permission_classes = [AllowAny]  # Разрешаем доступ всем, даже неавторизованным

    def post(self, request) -> Response:
        """
        Регистрирует нового пользователя.
        Вход: username, email, password.
        Выход: данные пользователя и токен.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'user': serializer.data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """APIView для входа пользователя."""
    permission_classes = [AllowAny]  # Разрешаем доступ всем, даже неавторизованным

    def post(self, request) -> Response:
        """
        Аутентифицирует пользователя и возвращает токен.
        Вход: username, password.
        Выход: токен.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            return Response({'error': 'Неверные данные'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
        """APIView для работы с личным кабинетом."""
        permission_classes = [IsAuthenticated]  # Только авторизованные пользователи

        def get(self, request) -> Response:
            """Возвращает данные профиля."""
            profile = request.user.profile  # Получаем профиль текущего пользователя
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)

        def put(self, request) -> Response:
            """Обновляет данные профиля."""
            profile = request.user.profile
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        def delete(self, request) -> Response:
            """Удаляет профиль и пользователя."""
            user = request.user
            user.delete()  # Удаляет и профиль, и пользователя из-за CASCADE
            return Response(status=status.HTTP_204_NO_CONTENT)