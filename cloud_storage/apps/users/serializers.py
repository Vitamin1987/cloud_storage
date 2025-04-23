from rest_framework import serializers
from django.contrib.auth.models import User
from apps.users.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели User."""
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

class UserProfileSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели UserProfile."""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'bio', 'created_at']
        read_only_fields = ['id', 'username', 'created_at']

    def update(self, instance: UserProfile, validated_data: dict) -> UserProfile:
        """Обновляет профиль и email пользователя."""
        user_data = validated_data.pop('user', {})
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()

        if 'email' in user_data:
            instance.user.email = user_data['email']
            instance.user.save()

        return instance