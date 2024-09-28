import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, FileResponse

from pdfform.views import validate_file_id
from pdfform.models import FileForProccess


@csrf_exempt
def view_result(request, fileID):
    if request.method == 'GET':
        if validate_file_id(fileID) is None:
            return JsonResponse({'error': 'Not existing file id'}, status=405)
        
        file = FileForProccess.objects.get(file_id=fileID)
        if file and file.is_ready and os.path.exists(FileForProccess.file_path + '/' + file.filename) and \
                    os.path.isfile(FileForProccess.file_path + '/' + file.filename):
                return FileResponse(open(FileForProccess.file_path + '/' + file.filename, 'rb'))
        
        return JsonResponse({'status': 'proccessing'})
    else:
        return JsonResponse({'error': 'Only GET method is allowed'}, status=405)
