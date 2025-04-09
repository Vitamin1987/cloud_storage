from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    """Модель местоположения клиента."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='locations')
    # Связь с пользователем
    ip_address = models.CharField(max_length=45)  # IP-адрес (поддерживает IPv6)
    city = models.CharField(max_length=100, blank=True, null=True)  # Город
    country = models.CharField(max_length=100, blank=True, null=True)  # Страна
    last_updated = models.DateTimeField(auto_now=True)  # Дата обновления

    def __str__(self) -> str:
        return f"{self.user.username} - {self.city}, {self.country}"

    class Meta:
        verbose_name = "Местоположение"
        verbose_name_plural = "Местоположения"