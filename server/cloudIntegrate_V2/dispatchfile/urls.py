#Required for api endpoint
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FileUploadViewSet

from . import downloader

# router = DefaultRouter()
# router.register(r'uploads', FileUploadViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('check-file/', downloader.check_file, name='check-file'),
    path('download/<str:file_name>/', downloader.download_file, name='download-file'),
]