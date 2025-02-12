import os
import threading
import time
import zipfile
import requests
from pathlib import Path
# from .models import FileUpload
from .models import DispatchInfo, ProcessedFolder
from fileupload.models import FileUploadMetadata
from threading import Lock
from django.db.models import Q


WATCHED_DIR = '/home/paperspace/koustav/server/draw-seg-v3_021224/output/TSPrime/results'
ZIPPED_DIR = '/home/paperspace/koustav/server/draw-seg-v3_021224/output/TSPrime/zippedForServer/'
#UPLOAD_URL = 'http://127.0.0.1:8080/upload'  # s1-endpoint
# UPLOAD_URL = 'http://10.5.29.232:8080/upload'  # s1-endpoint
# UPLOAD_URL = 'http://203.110.242.11:8080/upload'  # s1-endpoint
UPLOAD_URL = 'http://100.123.93.217:8080/upload'  # s1-endpoint (using netbird)

# lock = Lock()
LOCK = threading.Lock()

currently_processing = set()  # Keep track of folders being processed

def start_watcher():
    while True:
        with LOCK:
            for folder_name in os.listdir(WATCHED_DIR):
                folder_path = os.path.join(WATCHED_DIR, folder_name)

                if os.path.isdir(folder_path):
                    # Check if the folder has been processed
                    if ProcessedFolder.objects.filter(folder_name=folder_name).exists():
                        #print(f"Skipping already processed folder: {folder_name}")
                        time.sleep(30)
                        continue  # Skip this folder if it's already processed
                    
                    print(f"Processing folder: {folder_name}")
                    
                    # Wait before zipping to ensure folder is fully populated
                    time.sleep(30)  # Delay to let folder be populated fully

                    # Iterate over all subdirectories within the main folder
                    sub_dir_names = []
                    ok = 1
                    for root, dirs, _ in os.walk(folder_path):
                        for dir_name in dirs:
                            sub_dir_names.append(dir_name)
                            if len(sub_dir_names) != 1:
                                ok = 0
                                print("Found unexpected number of items in root folder.")
                    
                    if ok:
                        zip_name = f"{folder_name}.zip"
                        zip_path = os.path.join(ZIPPED_DIR, zip_name)
                        print("Zip path:", zip_path)

                        # Create 'zippedForServer' directory if it doesn't exist
                        os.makedirs(os.path.dirname(zip_path), exist_ok=True)

                        try:
                            # Zip the folder
                            with zipfile.ZipFile(zip_path, 'w') as zipf:
                                for root, _, files in os.walk(folder_path):
                                    for file in files:
                                        zipf.write(os.path.join(root, file),
                                                   os.path.relpath(os.path.join(root, file), folder_path))

                            time.sleep(5)  # Delay after zipping

                            # Update the processing_status field for the specific zip_file_name
                            print("Updating processing_status and result_path for zip_file_name:", (sub_dir_names[0].split('.'))[0])
                            FileUploadMetadata.objects.filter(zip_file_name=(sub_dir_names[0].split('.'))[0]).update(
                                processing_status='done', result_path=zip_path)

                            # Mark this folder as processed
                            #ProcessedFolder.objects.create(folder_name=folder_name)

                            # Mark this folder as processed (use get_or_create to avoid duplicates)
                            ProcessedFolder.objects.get_or_create(folder_name=folder_name)
                        
                        except Exception as e:
                            print(f"Error processing {folder_name}: {e}")
                        finally:
                            pass
                    else:
                        print("Unexpected sub-directories in root folder.")
                
        # Sleep for a short time to reduce load on the system before checking again
        time.sleep(10)




####################################################################################################################
#Everything is fine in this version, except the fact that multiple attempts are being made for each folder. Specifically 2.
#But in terms of output wise there is no difference and also in DB there is only one entry.

# lock = Lock()  # Ensure thread safety

# def start_watcher():
#     # Ensure the zippedForServer directory exists
#     if not os.path.exists(ZIPPED_DIR):
#         os.makedirs(ZIPPED_DIR)

#     while True:
#         with lock:
#             for folder_name in os.listdir(WATCHED_DIR):
#                 folder_path = os.path.join(WATCHED_DIR, folder_name)
#                 zip_name = f"{folder_name}.zip"
#                 zip_path = os.path.join(ZIPPED_DIR, zip_name)

#                 # Check if the folder is a directory and has not been processed or has 'Pending' status
#                 if os.path.isdir(folder_path) and not DispatchInfo.objects.filter(
#                         Q(folder_name=folder_name) & Q(status='Sent')).exists():

#                     try:
#                         # Zip the folder in the new directory
#                         with zipfile.ZipFile(zip_path, 'w') as zipf:
#                             for root, _, files in os.walk(folder_path):
#                                 for file in files:
#                                     zipf.write(os.path.join(root, file),
#                                                os.path.relpath(os.path.join(root, file), folder_path))

#                         # Get or create the record for this folder (to avoid duplication)
#                         file_upload, created = DispatchInfo.objects.get_or_create(
#                             folder_name=folder_name,
#                             defaults={'zip_name': zip_name, 'status': 'Pending'}
#                         )

#                         # If not created, it means the entry exists, update the zip_name and status
#                         if not created:
#                             file_upload.zip_name = zip_name
#                             file_upload.status = 'Pending'
#                             file_upload.save()

#                         # Introduce delay to ensure zipping is complete before uploading
#                         time.sleep(3)

#                         # Upload the zip file to s1
#                         with open(zip_path, 'rb') as zip_file:
#                             file_name = os.path.basename(zip_path)
#                             files = {'file': (file_name, zip_file)}
#                             headers = {'Content-Disposition': f'attachment; filename="{file_name}"'}
#                             print(f"Uploading file {zip_name} to {UPLOAD_URL}...")
#                             response = requests.post(UPLOAD_URL, files=files, headers=headers)
#                             print(f"Received response: {response.status_code}")

#                         # Update status in DB based on response
#                         if response.status_code == 200:
#                             file_upload.status = 'Sent'
#                         else:
#                             file_upload.status = 'Failed'

#                         file_upload.save()

#                     except Exception as e:
#                         print(f"Error processing {folder_name}: {e}")

#         time.sleep(10)  # Check every 10 seconds


#############################################################################################################################



# WATCHED_DIR = '/home/koustav/Work/Pipeline/draw-seg/output/TSPrime/results/'
# UPLOAD_URL = 'http://127.0.0.1:8080/upload'  #'http://s1-endpoint-url/upload/'

# lock = Lock()  # Use a lock to ensure thread safety

# def start_watcher():
#     processed_folders = set()
#     while True:
#         with lock:
#             for folder_name in os.listdir(WATCHED_DIR):
#                 folder_path = os.path.join(WATCHED_DIR, folder_name)
#                 if os.path.isdir(folder_path) and folder_name not in processed_folders:
#                     zip_name = f"{folder_name}.zip"
#                     zip_path = os.path.join(WATCHED_DIR, zip_name)

#                     try:
#                         # Zip the folder
#                         with zipfile.ZipFile(zip_path, 'w') as zipf:
#                             for root, _, files in os.walk(folder_path):
#                                 for file in files:
#                                     zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), folder_path))

#                         # Save details in DB (set initial status as 'Pending')
#                         file_upload = DispatchInfo.objects.create(
#                             folder_name=folder_name,
#                             zip_name=zip_name,
#                             status='Pending'
#                         )

#                         # Upload to deidentificationSystem
#                         with open(zip_path, 'rb') as zip_file:
#                             # response = requests.post(UPLOAD_URL, files={'file': zip_file})
#                             file_name = os.path.basename(zip_path)  # Get the actual file name
#                             files = {'file': (file_name, zip_file)}
#                             headers = {'Content-Disposition': f'attachment; filename="{file_name}"'}
#                             print(f"Uploading file {zip_name} to {UPLOAD_URL}...")
#                             response = requests.post(UPLOAD_URL, files=files, headers=headers)
#                             print(f"Received response: {response.status_code}")

#                         # Handle response from deidentificationSystem
#                         if response.status_code == 200:
#                             file_upload.status = 'Sent'
#                         else:
#                             file_upload.status = 'Failed'

#                         file_upload.save()

#                         processed_folders.add(folder_name)

#                     except Exception as e:
#                         print(f"Error processing {folder_name}: {e}")

#         time.sleep(5)  # Check every 10 seconds
