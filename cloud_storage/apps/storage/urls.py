from django.urls import path
from apps.storage.views import (
    FolderListCreateView, FolderDetailView,
    FileListCreateView, FileDetailView,
    StorageListCreateView, StorageDetailView
)

urlpatterns = [
    path('storages/', StorageListCreateView.as_view(), name='storage-list-create'),
    path('storages/<int:pk>/', StorageDetailView.as_view(), name='storage-detail'),
    path('folders/', FolderListCreateView.as_view(), name='folder-list-create'),
    path('folders/<int:pk>/', FolderDetailView.as_view(), name='folder-detail'),
    path('files/', FileListCreateView.as_view(), name='file-list-create'),
    path('files/<int:pk>/', FileDetailView.as_view(), name='file-detail'),
]