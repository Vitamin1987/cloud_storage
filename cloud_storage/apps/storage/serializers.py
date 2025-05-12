from rest_framework import serializers
from apps.storage.models import Folder, File, Storage


class StorageSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Storage."""
    class Meta:
        model = Storage
        fields = ['id', 'name', 'owner', 'created_at']
        read_only_fields = ['owner', 'created_at']


class FolderSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Folder."""
    class Meta:
        model = Folder
        fields = ['id', 'name', 'owner', 'storage', 'parent', 'created_at']
        read_only_fields = ['owner', 'created_at']

    def validate(self, attrs: dict) -> dict:
        """Проверяет, что родительская папка и хранилище принадлежат пользователю."""
        request = self.context['request']
        storage = attrs.get('storage')
        parent = attrs.get('parent')

        if storage and storage.owner != request.user:
            raise serializers.ValidationError("Вы не можете использовать чужое хранилище.")
        if parent and parent.owner != request.user:
            raise serializers.ValidationError("Вы не можете использовать чужую папку как родительскую.")
        return attrs


class FileSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели File."""
    class Meta:
        model = File
        fields = ['id', 'name', 'owner', 'folder', 'file', 'size', 'uploaded_at']
        read_only_fields = ['owner', 'size', 'uploaded_at']

    def validate_folder(self, value: Folder) -> Folder:
        """Проверяет, что папка принадлежит пользователю."""
        if value and value.owner != self.context['request'].user:
            raise serializers.ValidationError("Вы не можете загружать файлы в чужую папку.")
        return value

    def create(self, validated_data: dict) -> File:
        """Создаёт файл и устанавливает размер."""
        file_instance = File(**validated_data)
        file_instance.size = file_instance.file.size
        file_instance.save()
        return file_instance