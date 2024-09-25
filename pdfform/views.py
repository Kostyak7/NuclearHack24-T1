from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .forms import UploadFileForm
from .models import FileForPrint
import datetime
from uuid import uuid4
from random import randint
import os
import pytz
from django.utils import timezone


class PrintFormView(View):
    def get(self, request, *args, **kwargs):
        return render(request, '_base_vue.html')


def handle_uploaded_file(f, params: dict) -> int:
    if not os.path.exists(FileForPrint.file_path):
        os.mkdir(FileForPrint.file_path)
    new_filename = str(uuid4()) + '.' + f.name.split('.')[-1].lower()
    while os.path.exists(FileForPrint.file_path + '/' + new_filename):
        new_filename = str(uuid4()) + '.' + f.name.split('.')[-1].lower()
    code = randint(100000, 999999)
    # print(FileForPrint.objects.filter(code_for_print=code))
    while FileForPrint.objects.filter(code_for_print=code):
        code = randint(100000, 999999)
        # print("Code:", code)
    with open(FileForPrint.file_path + '/' + new_filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    FileForPrint.objects.create(filename=new_filename, code_for_print=code, upload_time=timezone.now(),
                                color=params['color'], format=params['format'], amount=params['amount'])
    return code


def validate_params(data: dict):
    if 'color' not in data.keys() or 'format' not in data.keys() or 'amount' not in data.keys():
        print("IOF1")
        return False
    if data['color'] != 'BLACK' and data['color'] != 'COLOR':
        print("IOF4")
        return False
    if data['format'] != 'ONE-SIDE' and data['format'] != 'TWO-SIDE':
        print("IOF5")
        return False
    if int(data['amount']) > 10 or int(data['amount']) < 1:
        print("IOF6")
        return False
    return {
        'color': str(data['color']),
        'format': str(data['format']),
        'amount': int(data['amount']),
    }


def is_format(filename, format='pdf') -> bool:
    return filename.split('.')[-1].lower() == format


def validate_file(f) -> bool:
    return is_format(f.name) and f.size < 25*1024*1024


@csrf_exempt
def print_form_filled(request):
    print(request)
    if request.method == 'POST':
        params = validate_params({
            'color': request.GET.get('color', None),
            'format': request.GET.get('format', None),
            'amount': request.GET.get('amount', None),
        })
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid() and params and validate_file(request.FILES['file']):
            code = handle_uploaded_file(request.FILES['file'], params)
            return JsonResponse({"validate": True, "code": code})
    return JsonResponse({"validate": False, "code": None})


def validate_code(code):
    if code is not None and FileForPrint.objects.filter(code_for_print=int(code)):
        return int(code)
    return None


class PrintCodeView(View):
    def get(self, request, *args, **kwargs):
        data = {
            "code": validate_code(request.GET.get('code', None)),
        }
        return render(request, '_base_vue.html', data)


# @csrf_exempt
def remove_expired(request):
    amount = 0
    if not os.path.exists(FileForPrint.file_path):
        return JsonResponse({"Amount": amount})
    check_time = timezone.localtime()
    for file in FileForPrint.objects.all():
        toRemove = False
        if (file.upload_time + datetime.timedelta(seconds=1)) < check_time: # hours=12   seconds=1
            if os.path.exists(FileForPrint.file_path + '/' + file.filename) and os.path.isfile(FileForPrint.file_path + '/' + file.filename):
                os.remove(FileForPrint.file_path + '/' + file.filename)
            toRemove = True
        if not os.path.exists(FileForPrint.file_path + '/' + file.filename):
            toRemove = True
        if toRemove:
            file.delete()
            amount += 1
    for filename in os.listdir(FileForPrint.file_path):
        if FileForPrint.objects.filter(filename=filename):
            if os.path.isfile(FileForPrint.file_path + '/' + filename):
                os.remove(FileForPrint.file_path + '/' + filename)
            else:
                os.rmdir(FileForPrint.file_path + '/' + filename)
    return JsonResponse({"Amount": amount})
