from django.contrib.auth.models import User
from apps.storage.models import Storage, Folder


def assign_default_storage():
    """Создаёт хранилище для каждого пользователя и привязывает папки."""
    for user in User.objects.all():
        # Создаём хранилище, если его нет
        storage, created = Storage.objects.get_or_create(
            owner=user,
            defaults={'name': f'Хранилище {user.username}'}
        )
        # Привязываем все папки пользователя к этому хранилищу
        Folder.objects.filter(owner=user, storage__isnull=True).update(storage=storage)
        print(f"Хранилище для {user.username}: {storage.name}")


if __name__ == "__main__":
    assign_default_storage()