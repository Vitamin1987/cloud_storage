from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from apps.storage.models import Folder, File
from apps.storage.serializers import FolderSerializer, FileSerializer


class FolderListCreateView(APIView):
    """APIView для списка и создания папок."""
    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        """Возвращает список папок пользователя с поиском и сортировкой."""
        folders = Folder.objects.filter(owner=request.user)

        # Поиск по имени
        search_query = request.query_params.get('search', None)
        if search_query:
            folders = folders.filter(name__icontains=search_query)

        # Сортировка
        sort_by = request.query_params.get('sort', 'created_at')  # По умолчанию по дате
        sort_order = request.query_params.get('order', 'asc')     # asc или desc
        if sort_by in ['name', 'created_at']:
            if sort_order == 'desc':
                folders = folders.order_by(f'-{sort_by}')
            else:
                folders = folders.order_by(sort_by)

        serializer = FolderSerializer(folders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request) -> Response:
        """Создаёт новую папку."""
        serializer = FolderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FolderDetailView(APIView):
    """APIView для работы с конкретной папкой."""
    permission_classes = [IsAuthenticated]

    def get_object(self, pk: int) -> Folder:
        try:
            folder = Folder.objects.get(pk=pk)
            if folder.owner != self.request.user:
                raise PermissionError("Это не ваша папка.")
            return folder
        except Folder.DoesNotExist:
            raise ValueError("Папка не найдена.")

    def get(self, request, pk: int) -> Response:
        folder = self.get_object(pk)
        serializer = FolderSerializer(folder)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk: int) -> Response:
        folder = self.get_object(pk)
        serializer = FolderSerializer(folder, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk: int) -> Response:
        folder = self.get_object(pk)
        folder.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FileListCreateView(APIView):
    """APIView для списка и создания файлов."""
    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        """Возвращает список файлов пользователя с поиском и сортировкой."""
        files = File.objects.filter(owner=request.user)

        # Поиск по имени
        search_query = request.query_params.get('search', None)
        if search_query:
            files = files.filter(name__icontains=search_query)

        # Сортировка
        sort_by = request.query_params.get('sort', 'uploaded_at')  # По умолчанию по дате
        sort_order = request.query_params.get('order', 'asc')      # asc или desc
        if sort_by in ['name', 'uploaded_at', 'size']:
            if sort_order == 'desc':
                files = files.order_by(f'-{sort_by}')
            else:
                files = files.order_by(sort_by)

        serializer = FileSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request) -> Response:
        """Создаёт новый файл."""
        serializer = FileSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileDetailView(APIView):
    """APIView для работы с конкретным файлом."""
    permission_classes = [IsAuthenticated]

    def get_object(self, pk: int) -> File:
        try:
            file = File.objects.get(pk=pk)
            if file.owner != self.request.user:
                raise PermissionError("Это не ваш файл.")
            return file
        except File.DoesNotExist:
            raise ValueError("Файл не найден.")

    def get(self, request, pk: int) -> Response:
        file = self.get_object(pk)
        serializer = FileSerializer(file)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk: int) -> Response:
        file = self.get_object(pk)
        serializer = FileSerializer(file, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk: int) -> Response:
        file = self.get_object(pk)
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)