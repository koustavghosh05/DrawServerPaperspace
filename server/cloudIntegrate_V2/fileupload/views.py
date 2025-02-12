# from django.shortcuts import render

# # Create your views here.
# import requests
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework import status
# from .models import UploadedFile
# from .serializers import UploadedFileSerializer

# class FileUploadView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, *args, **kwargs):
#         print("Received POST request at /api/upload/")  # Debug print statement
#         file_serializer = UploadedFileSerializer(data=request.data)
#         if file_serializer.is_valid():
#             file_instance = file_serializer.save()

#             # Upload the file to the remote server
#             remote_server_url = 'http://127.0.0.1:8000/upload/'  # Change this as needed
#             with open(file_instance.file.path, 'rb') as f:
#                 response = requests.post(remote_server_url, files={'file': f})
#                 if response.status_code == 200:
#                     return Response(file_serializer.data, status=status.HTTP_201_CREATED)
#                 else:
#                     file_instance.delete()  # Remove the file instance if upload fails
#                     return Response({'error': 'Failed to upload to remote server'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# from django.http import JsonResponse

# # Existing imports
# import requests
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework import status
# from .models import UploadedFile
# from .serializers import UploadedFileSerializer

# class FileUploadView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, *args, **kwargs):
#         print("Received POST request at /api/upload/")  # Debug print statement
#         file_serializer = UploadedFileSerializer(data=request.data)
#         if file_serializer.is_valid():
#             file_instance = file_serializer.save()

#             # Upload the file to the remote server
#             remote_server_url = 'http://127.0.0.1:8000/api/remote-upload/'  # Change this as needed
#             with open(file_instance.file.path, 'rb') as f:
#                 response = requests.post(remote_server_url, files={'file': f})
#                 if response.status_code == 200:
#                     return Response(file_serializer.data, status=status.HTTP_201_CREATED)
#                 else:
#                     file_instance.delete()  # Remove the file instance if upload fails
#                     return Response({'error': 'Failed to upload to remote server'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class RemoteFileUploadView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, *args, **kwargs):
#         print("Received file upload at /api/remote-upload/")  # Debug print statement
#         # Save the uploaded file
#         file_serializer = UploadedFileSerializer(data=request.data)
#         if file_serializer.is_valid():
#             file_instance = file_serializer.save()
#             return JsonResponse({'message': 'File uploaded successfully'}, status=200)
#         else:
#             return JsonResponse({'error': 'Invalid file data'}, status=400)







#Safe state checkpoint, below
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework import status
# from .models import UploadedFile
# from .serializers import UploadedFileSerializer

# import os
# import zipfile
# from django.conf import settings
# import shutil


# def copy_last_level_dirs_to_SharedSpace(source_folder, dest_folder):
#     # Walk through the source folder recursively
#         for root, dirs, files in os.walk(source_folder):
#             # If there are files and no subdirectories, it's the last level
#             if files and not dirs:
#                 # Copy the last level directory
#                 folder_to_copy = root
#                 dest_path = os.path.join(dest_folder, os.path.basename(folder_to_copy))
#                 try:
#                     shutil.copytree(folder_to_copy, dest_path)
#                     # print(f"Copied {folder_to_copy} to {dest_path}")
#                     print("Copied to shared space")
#                 except Exception as e:
#                     print(f"Error copying {folder_to_copy}: {e}")


# class FileUploadView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     # def post(self, request, *args, **kwargs):
#     #     print("Received POST request at /api/upload/")  # Debug print statement
#     #     file_serializer = UploadedFileSerializer(data=request.data)
#     #     if file_serializer.is_valid():
#     #         file_serializer.save()
#     #         return Response(file_serializer.data, status=status.HTTP_201_CREATED)
#     #     else:
#     #         return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     def post(self, request, *args, **kwargs):
#         print("Received POST request at /api/upload/")  # Debug print statement
#         file_serializer = UploadedFileSerializer(data=request.data)
#         if file_serializer.is_valid():
#             file_instance = file_serializer.save()

#             # Path to the uploaded file
#             zip_file_path = file_instance.file.path

#             # Directory where the ZIP file is located
#             zip_file_dir = os.path.dirname(zip_file_path)

#             # Unzip the file
#             if zipfile.is_zipfile(zip_file_path):
#                 with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
#                     zip_ref.extractall(zip_file_dir)  # Extract to the same directory where the ZIP file is located
#                     extracted_item = zip_ref.namelist()[0]
#                     source_dir_toCopyFrom=zip_file_dir + '/' + extracted_item + '/'
#                     dest_dir_sharedSpace="/home/koustav/Work/Pipeline/shared_space/" #Modify as per requirement. Later make seperate config file
#                     copy_last_level_dirs_to_SharedSpace(source_dir_toCopyFrom, dest_dir_sharedSpace)

#                 # Delete the original zip file after extraction
#                 os.remove(zip_file_path)
#                 print("Unzipped and deleted the file")
#                 # print(f"Unzipped and deleted the file: {zip_file_path}")

#             return Response(file_serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)








#Slight modifications to the above code for edge case handling
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import UploadedFile
from .serializers import UploadedFileSerializer

import os
import zipfile
from django.conf import settings
import shutil

import logging
from django.db import transaction


# Initialize logging
logger = logging.getLogger(__name__)


def copy_last_level_dirs_to_SharedSpace(source_folder, dest_folder):
    try:
        # Walk through the source folder recursively
        for root, dirs, files in os.walk(source_folder):
            # If there are files and no subdirectories, it's the last level
            if files and not dirs:
                # Copy the last level directory
                folder_to_copy = root
                dest_path = os.path.join(dest_folder, os.path.basename(folder_to_copy))

                # Check if the folder already exists at the destination
                if os.path.exists(dest_path):
                    try:
                        # If the folder exists, remove it and then copy
                        shutil.rmtree(dest_path)  # Removes the folder if it exists
                        print(f"Removed existing folder: {dest_path}")
                    except Exception as e:
                        print(f"Error removing existing folder {dest_path}: {e}")
                        continue  # Skip this folder if removal fails

                try:
                    # Now copy the folder to the destination
                    shutil.copytree(folder_to_copy, dest_path)
                    print(f"Copied {folder_to_copy} to {dest_path}")
                    print("Copied to shared space")
                except Exception as e:
                    print(f"Error copying {folder_to_copy}: {e}")
    except Exception as ex:
        logger.error(f"Error parsing through the source folder: {ex}")

from .models import FileUploadMetadata
from datetime import datetime
from pathlib import Path
from django.utils import timezone
from dispatchfile.models import DispatchInfo

from django.http import JsonResponse, FileResponse
import uuid
import hashlib

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    # def post(self, request, *args, **kwargs):
    #     print("Received POST request at /api/upload/")  # Debug print statement
    #     file_serializer = UploadedFileSerializer(data=request.data)
    #     if file_serializer.is_valid():
    #         file_serializer.save()
    #         return Response(file_serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @transaction.atomic  # Ensure the DB operations are atomic
    def post(self, request, *args, **kwargs):
        logger.info("Received POST request at /api/upload/")
        print("Received POST request at /api/upload/")  # Debug print statement
        file_serializer = UploadedFileSerializer(data=request.data)

        # Extract IP and port from request
        # ip_address = request.META.get('REMOTE_ADDR', '')
        client_ip = request.headers.get('X-Client-IP', request.META.get('REMOTE_ADDR'))
        # port_no = request.META.get('REMOTE_PORT', 0)
        client_port = request.headers.get('X-Client-Port', request.META.get('REMOTE_PORT'))
        print(f"Request received from IP: {client_ip}, Port: {client_port}")
        # logger.info(f"Request received from IP: {client_ip}, Port: {client_port}")
        
        if file_serializer.is_valid():
            try:
                file_instance = file_serializer.save()

                # Path to the uploaded file
                zip_file_path = file_instance.file.path
                zip_name = Path(zip_file_path).name

                # Generate a unique token
                unique_id = str(uuid.uuid4())
                file_hash = hashlib.sha256(unique_id.encode()).hexdigest()


                # Save metadata to the database
                FileUploadMetadata.objects.create(
                    datetime_of_creation=timezone.now(),
                    ip_address=client_ip,
                    port_no=client_port,
                    zip_file_name= (str(os.path.basename(zip_name)))[:-4], # .basename returns '92612202400000_zip' Hence excluding last 4 char
                    file_token=file_hash  # Save the unique token in the database
                )

                # Directory where the ZIP file is located
                zip_file_dir = os.path.dirname(zip_file_path)
                # print(f"zip_file_path:{zip_file_path}")
                # print(f"zip_name:{zip_name}")

                # Unzip the file
                if zipfile.is_zipfile(zip_file_path):
                    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                        zip_ref.extractall(zip_file_dir)  # Extract to the same directory where the ZIP file is located
                        extracted_item = zip_ref.namelist()[0]

                        # Build source and destination paths
                        source_dir_toCopyFrom=zip_file_dir + '/' + extracted_item + '/'
                        # dest_dir_sharedSpace="/home/koustav/Work/Pipeline/shared_space/" #Modify as per requirement. Later make seperate config file
                        dest_dir_sharedSpace=os.path.join(settings.SHARED_SPACE_PATH, 'shared_space/')  # Configure in settings
                        copy_last_level_dirs_to_SharedSpace(source_dir_toCopyFrom, dest_dir_sharedSpace)

                    # Delete the original zip file after extraction
                    os.remove(zip_file_path)
                    print("Unzipped and deleted the file")
                    # print(f"Unzipped and deleted the file: {zip_file_path}")
                
                # Send JSON response with token
                response_data = {
                    "message": "Upload successfull.",
                    "file_token": file_hash,
                    "file_name": zip_name,
                }
                return JsonResponse(response_data, status=status.HTTP_201_CREATED)
                #return Response(file_serializer.data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                logger.error(f"Error processing file upload: {e}")
                return Response({"error": "File processing failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
