from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from builder.services import handle_file
from builder.forms import UploadFileForm
from builder.models import UploadFile
from builder.services import get_excel_subjects

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
        print(form.errors)
        if form.is_valid():
            file = UploadFile(file=request.FILES['file'], owner=request.user)
            file.save()
            print(UploadFile.objects.last())

        response_dict = {
            'message': 'File uploaded successfully!',
        }

        return JsonResponse(response_dict, status=200)


def subj(request):
    if request.method == 'GET':

        path = str(UploadFile.objects.filter(owner=request.user).last().file)
        response = get_excel_subjects(path)

        return JsonResponse(response, status=200, safe=False)
