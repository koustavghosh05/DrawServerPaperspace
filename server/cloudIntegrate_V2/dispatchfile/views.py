#Required for api endpoint

from django.shortcuts import render

from rest_framework import viewsets
from .models import DispatchInfo
from .serializers import DispatchInfoSerializer

# Create your views here.
class FileUploadViewSet(viewsets.ModelViewSet):
    queryset = DispatchInfo.objects.all().order_by('-timestamp')
    serializer_class=DispatchInfoSerializer
