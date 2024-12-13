from django.urls import path
from .views import IndexView, FileListView, DownloadFileView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('files/', FileListView.as_view(), name='files_list'),
    path('download/', DownloadFileView.as_view(), name='download_file'),
]
