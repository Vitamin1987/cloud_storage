from django.contrib import admin
from apps.storage.models import Storage, Folder, File


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    """Админ-панель для модели Storage."""
    list_display = ('name', 'owner', 'created_at')  # Поля для отображения в списке
    list_filter = ('owner',)  # Фильтр по владельцу
    search_fields = ('name',)  # Поиск по имени


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    """Админ-панель для модели Folder."""
    list_display = ('name', 'owner', 'storage', 'parent', 'created_at')
    list_filter = ('owner', 'storage')
    search_fields = ('name',)


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    """Админ-панель для модели File."""
    list_display = ('name', 'owner', 'folder', 'size', 'uploaded_at')
    list_filter = ('owner', 'folder')
    search_fields = ('name',)