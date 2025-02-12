from django.db import models

#FileUpload
# Create your models here.
class DispatchInfo(models.Model):
    folder_name = models.CharField(max_length=255)
    zip_name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='Pending')  # Pending, Sent, Failed
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.folder_name} ({self.zip_name}) - {self.status}"


class ProcessedFolder(models.Model):
    folder_name = models.CharField(max_length=255, unique=True)
    processed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.folder_name