from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.location.models import Location
from apps.location.serializers import LocationSerializer
import requests


class LocationView(APIView):
    """APIView для получения и обновления местоположения клиента."""
    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        """Возвращает последнее местоположение пользователя."""
        location = Location.objects.filter(user=request.user).order_by('-last_updated').first()
        if location:
            serializer = LocationSerializer(location)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Местоположение ещё не определено"}, status=status.HTTP_404_NOT_FOUND)


def update_user_location(request) -> None:
    """Обновляет местоположение пользователя по IP."""
    # Получаем IP клиента
    ip = request.META.get('REMOTE_ADDR', '127.0.0.1')  # Для локального тестирования будет 127.0.0.1
    if ip == '127.0.0.1':
        # Для теста можно использовать заглушку
        ip = '8.8.8.8'  # Пример реального IP

    # Запрос к стороннему API
    try:
        response = requests.get(f'https://ipapi.co/{ip}/json/')
        response.raise_for_status()
        data = response.json()
        city = data.get('city', 'Неизвестно')
        country = data.get('country_name', 'Неизвестно')
    except requests.RequestException:
        city, country = 'Неизвестно', 'Неизвестно'

    # Сохраняем или обновляем местоположение
    Location.objects.update_or_create(
        user=request.user,
        ip_address=ip,
        defaults={'city': city, 'country': country}
    )