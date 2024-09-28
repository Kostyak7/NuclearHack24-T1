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


class FileFormView(View):
    def get(self, request, *args, **kwargs):
        return render(request, '_base_vue.html')


def handle_uploaded_file(f, params: dict) -> str:
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
    FileForProccess.objects.create(filename=new_filename, file_id=fileID, upload_time=timezone.now(), lang=params['lang'])
    return fileID


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
            'lang': request.GET.get('lang', None),
        })
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid() and params and validate_file(request.FILES['file']):
            fileID = handle_uploaded_file(request.FILES['file'], params)
            return JsonResponse({"validate": True, "fileID": fileID})
    return JsonResponse({"validate": False, "fileID": None})


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
