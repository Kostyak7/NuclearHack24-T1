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
        filename_start = FileForProccess.file_path + '/' + file.filename
        if file and file.is_ready and os.path.exists(filename_start) and os.path.isfile(filename_start):
                result_filename = os.path.splitext(filename_start)[0] + '_output.pdf'
                if os.path.exists(result_filename) and os.path.isfile(result_filename):
                    return FileResponse(open(result_filename, 'rb'))     
                return FileResponse(open(filename_start, 'rb'))
        
        return JsonResponse({'status': 'proccessing'})
    else:
        return JsonResponse({'error': 'Only GET method is allowed'}, status=405)
