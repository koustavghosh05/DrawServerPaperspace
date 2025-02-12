from rest_framework import serializers
from .models import DispatchInfo

class DispatchInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DispatchInfo
        fields = ['id', 'folder_name', 'zip_name', 'status', 'timestamp']