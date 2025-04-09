from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Модель профиля пользователя для личного кабинета."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # Связь один-к-одному с встроенной моделью User
    bio = models.TextField(max_length=500, blank=True, null=True)  # Описание профиля
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    def __str__(self) -> str:
        return f"Профиль {self.user.username}"

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"
