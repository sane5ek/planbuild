from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.encoding import smart_str

from .forms import UploadFileForm
from .models import UploadFile, Subject, Field

import json
# Create your views here.

from django.http import HttpResponse


def index(request, template_name='builder/index.html'):
    if not request.user.is_authenticated:
        return redirect('builder_auth:login')
    else:
        return render(request, 'builder/index.html')


def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = UploadFile(file=request.FILES['file'], owner=request.user)
            new_file.save()
            new_file.convert_file_to_xlsx()

        response_dict = {
            'message': 'File uploaded successfully!',
        }

        return JsonResponse(response_dict, status=200)


def subj(request):
    if request.method == 'GET':
        path = UploadFile.objects.filter(owner=request.user).last().file.name
        Subject.objects.set_objects_from_excel(path, request.user)
        response = Subject.objects.get_objects_json(request.user)

        return JsonResponse(response, status=200, safe=False)


def build(request):
    if request.method == 'POST':
        subjects = json.loads(request.POST['subjects']) # list of dicts
        course = json.loads(request.POST['course'])
        diploma = json.loads(request.POST['diploma'])
        load_path = UploadFile.objects.filter(owner=request.user).last().file.name
        template_path = 'files/Template.xlsx'

        Field.objects.FillTemplate(subjects, course, diploma, load_path, template_path, request.user)

        # path_to_file = 'D:\\Programming\\Projects\\python\\PlanBuild\\333\\!0_Котенко_1_5_Индивидуальный план работы преподавателя.xls'
        # with open(path_to_file,'rb') as f:
        #     data = f.read()
        # response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(path_to_file)
        response = HttpResponse('ss')
        return response
