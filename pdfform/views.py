from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .forms import UploadFileForm
from .models import FileForProccess
import datetime
from uuid import uuid4
import os
from django.utils import timezone

from .proccess_async import process_form_data_async


class FileFormView(View):
    def get(self, request, *args, **kwargs):
        return render(request, '_base_vue.html')


def handle_uploaded_file(f, params: dict) -> list:
    if not os.path.exists(FileForProccess.file_path):
        os.mkdir(FileForProccess.file_path)
        
    fileID = str(uuid4())
    new_filename = fileID + '.' + f.name.split('.')[-1].lower()
    while os.path.exists(FileForProccess.file_path + '/' + new_filename):
        fileID = str(uuid4())
        new_filename = fileID + '.' + f.name.split('.')[-1].lower()
        
    with open(FileForProccess.file_path + '/' + new_filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    db_object = None
    toc_range = [
        -1 if params["toc_range"][0] is None else params["toc_range"][0],
        -1 if params["toc_range"][1] is None else params["toc_range"][1],
    ]
    has_toc = params['has_toc']
    if has_toc is not None and has_toc and (toc_range[0] <= 0 or toc_range[1] <= 0 or toc_range[1] < toc_range[0]):
        has_toc = None
    db_object = FileForProccess.objects.create(filename=new_filename, 
                                               file_id=fileID, 
                                               upload_time=timezone.now(), 
                                               lang=params['lang'], 
                                               has_toc_hint=has_toc,
                                               toc_start_hint=toc_range[0],
                                               toc_end_hint=toc_range[1])
    return [fileID, db_object]


def validate_params(data: dict):
    keys = data.keys()
    if 'lang' not in keys or data['lang'] != 'RUS' and data['lang'] != 'ENG':
        return False
    return {
        'lang': str(data['lang']),
    }


def is_format(filename, format='pdf') -> bool:
    return filename.split('.')[-1].lower() == format


def validate_file(f) -> bool:
    return is_format(f.name) and f.size < 25*1024*1024


@csrf_exempt
def file_form_filled(request):
    print(request)
    if request.method == 'POST':
        params = validate_params({
            'lang': request.GET.get('lang', 'RUS'),

            'has_toc': request.GET.get('has_toc_hint', None),
            'toc_range': [
                request.GET.get('toc_range_start_hint', None), 
                request.GET.get('toc_range_end_hint', None)
                ]
        })
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid() and params and validate_file(request.FILES['file']):
            fileID, db_object = handle_uploaded_file(request.FILES['file'], params)
            process_form_data_async(db_object.id) # здесь вызываем алгоритм
            return JsonResponse({"validate": True, "fileID": fileID}, status=201)
    return JsonResponse({"validate": False, "fileID": None}, status=405)


def validate_file_id(fileID):
    if fileID is not None and FileForProccess.objects.filter(file_id=fileID):
        return fileID
    return None


class FileIDView(View):
    def get(self, request, *args, **kwargs):
        data = {
            "fileID": validate_file_id(request.GET.get('fileID', None)),
        }
        return render(request, '_base_vue.html', data)


# @csrf_exempt
def remove_expired(request):
    amount = 0
    if not os.path.exists(FileForProccess.file_path):
        return JsonResponse({"Amount": amount})
    check_time = timezone.localtime()
    for file in FileForProccess.objects.all():
        toRemove = False
        if (file.upload_time + datetime.timedelta(seconds=1)) < check_time: # hours=12   seconds=1
            if os.path.exists(FileForProccess.file_path + '/' + file.filename) and os.path.isfile(FileForProccess.file_path + '/' + file.filename):
                os.remove(FileForProccess.file_path + '/' + file.filename)
            toRemove = True
        if not os.path.exists(FileForProccess.file_path + '/' + file.filename):
            toRemove = True
        if toRemove:
            file.delete()
            amount += 1
    for filename in os.listdir(FileForProccess.file_path):
        if FileForProccess.objects.filter(filename=filename):
            if os.path.isfile(FileForProccess.file_path + '/' + filename):
                os.remove(FileForProccess.file_path + '/' + filename)
            else:
                os.rmdir(FileForProccess.file_path + '/' + filename)
    return JsonResponse({"Amount": amount})
