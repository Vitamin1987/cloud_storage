from django.db import models
from django.contrib.auth.models import User


class Folder(models.Model):
    """Модель папки в облачном хранилище."""
    name = models.CharField(max_length=255)  # Название папки
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders')
    # Связь с пользователем (владелец)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subfolders')
    # Связь с родительской папкой (для вложенности)
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Папка"
        verbose_name_plural = "Папки"


class File(models.Model):
    """Модель файла в облачном хранилище."""
    name = models.CharField(max_length=255)  # Название файла
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    # Связь с пользователем (владелец)
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, null=True, blank=True, related_name='files')
    # Связь с папкой (где лежит файл)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')  # Путь к файлу
    size = models.PositiveIntegerField(default=0)  # Размер файла в байтах
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Дата загрузки

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"