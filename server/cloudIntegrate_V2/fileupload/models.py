from django.db import models
from django.utils.timezone import now

# Create your models here.
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


# New model for metadata
class FileUploadMetadata(models.Model):
    datetime_of_creation = models.DateTimeField(default=now)  # Timestamp
    ip_address = models.GenericIPAddressField()              # IP Address
    port_no = models.IntegerField()                          # Port number
    zip_file_name = models.CharField(max_length=255)         # File name
    file_token = models.CharField(max_length=255, blank=True, null=True)            #File token

    # New field for processing status
    PROCESSING_STATUS_CHOICES = [
        ('pending', 'In Queue'), #(value_stored_in_db, Human readable values)
        ('done', 'Segmentation Done'),
        ('file_sent', 'File Sent'),
    ]

    processing_status = models.CharField(
        max_length=20,
        choices=PROCESSING_STATUS_CHOICES,
        default='pending',  # Default status when a new record is created
    )

    # New field for result_path
    result_path = models.TextField(null=True, blank=True)  # Allows null and blank values for optional field
    #TextField: This field type allows for longer text than CharField, and it's appropriate for storing potentially long file paths.

    def __str__(self):
        return f"{self.zip_file_name} from {self.ip_address}:{self.port_no}"