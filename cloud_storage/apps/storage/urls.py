from django.urls import path
from apps.storage.views import FolderListCreateView, FolderDetailView, FileListCreateView, FileDetailView

urlpatterns = [
    path('folders/', FolderListCreateView.as_view(), name='folder-list-create'),
    path('folders/<int:pk>/', FolderDetailView.as_view(), name='folder-detail'),
    path('files/', FileListCreateView.as_view(), name='file-list-create'),
    path('files/<int:pk>/', FileDetailView.as_view(), name='file-detail'),
]