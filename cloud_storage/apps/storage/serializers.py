from rest_framework import serializers
from apps.storage.models import Folder, File


class FolderSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Folder."""
    class Meta:
        model = Folder
        fields = ['id', 'name', 'owner', 'parent', 'created_at']
        read_only_fields = ['owner', 'created_at']

    def validate_parent(self, value: Folder) -> Folder:
        """Проверяет, что родительская папка принадлежит тому же пользователю."""
        if value and value.owner != self.context['request'].user:
            raise serializers.ValidationError("Вы не можете использовать чужую папку как родительскую.")
        return value


class FileSerializer(serializers.ModelSerializer):
    """Сериализатор для модели File."""
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
        file_instance.size = file_instance.file.size  # Устанавливаем размер файла
        file_instance.save()
        return file_instance