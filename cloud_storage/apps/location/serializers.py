from rest_framework import serializers
from apps.location.models import Location


class LocationSerializer(serializers.ModelSerializer):
    """Сериалйзер для модели Location."""
    class Meta:
        model = Location
        fields = ['id', 'ip_address', 'city', 'country', 'last_updated']
        read_only_fields = ['id', 'ip_address', 'last_updated']