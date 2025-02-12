import os
from django.http import JsonResponse, FileResponse
from django.conf import settings
from fileupload.models import FileUploadMetadata
from django.shortcuts import get_object_or_404

# Directory where ready files are stored
# READY_FILES_DIR = os.path.join(settings.MEDIA_ROOT, 'ready_files')
# READY_FILES_DIR = "/home/koustav/Work/Pipeline/draw-seg-v3_021224/output/TSPrime/zippedForServer/"
READY_FILES_DIR = "/home/paperspace/koustav/server/draw-seg-v3_021224/output/TSPrime/zippedForServer"

def check_file(request):
    """
    Handles client requests for file availability by token.
    """
    # Extract token from the query parameters
    file_token = request.GET.get('token')

    if not file_token:
        return JsonResponse({'status': 'error', 'message': 'Token is missing from the request.'}, status=400)

    try:
        # Fetch the record from FileUploadMetadata by token
        metadata = FileUploadMetadata.objects.get(file_token=file_token)

        # Check the processing status
        if metadata.processing_status == 'done' and metadata.result_path:
            # File is ready for download
            result_zip_name = metadata.result_path.split('/')[-1]
            return JsonResponse({
                'status': 'file_ready',
                'file_name': metadata.zip_file_name,
                #'file_url': f"{request.scheme}://{request.get_host()}/dispatchfile/download/{file_token}/",
                'file_url': f"http://{request.get_host()}/dispatchfile/download/{file_token}/",
                # 'result_path': metadata.result_path
            }, status=200)
        elif metadata.processing_status == 'pending':
            # File is still in queue
            return JsonResponse({'status': 'pending', 'message': 'File is still being processed.'}, status=202)
        elif metadata.processing_status == 'file_sent':
            #File is already sent once, and deleted thereafter
            return JsonResponse({'status': 'sent', 'message': 'File is already sent once and no longer available in server.'}, status=202)
        else:
            # File not found or some unexpected status
            return JsonResponse({'status': 'error', 'message': 'File token not found in server DB'}, status=204)

    except FileUploadMetadata.DoesNotExist:
        # Token not found in the database
        return JsonResponse({'status': 'error', 'message': 'Invalid token or file not found.'}, status=404)



def download_file(request, file_name):
    """
    Handles the actual file download when the client requests the URL.
    """
    metadata = FileUploadMetadata.objects.get(file_token=file_name)

    # file_path = os.path.join(READY_FILES_DIR, file_name)
    file_path = metadata.result_path
    file_name = file_path.split('/')[-1]

    if not os.path.exists(file_path):
        return JsonResponse({'status': 'error', 'message': 'File not found.'}, status=404)

    # Serve the file to the client
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
