from rest_framework import serializers
from django.contrib.auth.models import User
from apps.users.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # Пароль не возвращается в ответе

    def create(self, validated_data: dict) -> User:
        """Создаёт нового пользователя и его профиль."""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        UserProfile.objects.create(user=user)  # Создаём профиль автоматически
        return user


class LoginSerializer(serializers.Serializer):
    """Сериалайзер для входа."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)