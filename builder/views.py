from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.encoding import smart_str
from django.forms import modelformset_factory
from django.forms import Select, TextInput
from django.utils import timezone

from .forms import UploadFileForm, FieldChangeForm
from .models import UploadFile, Subject, Field, PlanFile, Request, RequestType, RequestResultType
from builder_auth.models import CustomUser

import json
# Create your views here.

from django.http import HttpResponse


def index(request, template_name='builder/index.html'):
    if not request.user.is_authenticated:
        return redirect('builder_auth:login')
    else:
        return render(request, 'builder/index.html')


def upload_load(request):
    if request.method == 'POST' and request.user.is_authenticated:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = UploadFile(file=request.FILES['file'], owner=request.user)
            new_file.save()
            new_file.convert_file_to_xlsx()

        response_dict = {
            'message': 'File uploaded successfully!',
        }

        return JsonResponse(response_dict, status=200)


def get_subjects(request):
    if request.method == 'GET' and request.user.is_authenticated:
        path = UploadFile.objects.filter(owner=request.user).last().file.name
        Subject.objects.set_objects_from_excel(path, request.user)
        response = Subject.objects.get_objects_json(request.user)

        return JsonResponse(response, status=200, safe=False)


def build_plan(request):
    if request.method == 'POST' and request.user.is_authenticated:
        subjects = json.loads(request.POST['subjects'])  # list of dicts
        course = json.loads(request.POST['course'])
        diploma = json.loads(request.POST['diploma'])
        load_path = UploadFile.objects.filter(owner=request.user).last().file.name
        template_path = 'files/Template.xlsx'

        Field.objects.FillTemplate(subjects, course, diploma, load_path, template_path, request.user)

        path_to_file = PlanFile.objects.filter(owner=request.user).last().file.name
        with open(path_to_file, 'rb') as f:
            data = f.read()
        response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(path_to_file)

        return response


def edit_fields(request, template_name='builder/fields.html'):
    fields = Field.objects.select_related('type_of_load').filter(owner=request.user.adopted_fields)
    context = {}
    FieldFormSet = modelformset_factory(Field, fields=(
        'column_in_load', 'column_in_plan', 'name_in_load', 'name_in_plan', 'load_type', 'type_of_load', 'owner'),
                                        extra=0,
                                        exclude=('owner',),
                                        max_num=1,
                                        widgets={'type_of_load': TextInput()})
    formset = FieldFormSet(request.POST or None,
                           queryset=fields)
    if request.method == 'GET' and request.user.is_authenticated:
        context = {'forms': formset}
        return render(request, template_name, context)
    if request.method == 'POST' and request.user.is_authenticated:

        # если пользователь всё же нажал сохранить, то создаем ему новые поля из тех, которые у него были показаны
        if formset.is_valid():
            fields_to_save = []
            Field.objects.filter(owner=request.user).delete()
            for form in formset:
                if form.is_valid():
                    field = Field()
                    field.column_in_load = form.cleaned_data['column_in_load']
                    field.column_in_plan = form.cleaned_data['column_in_plan']
                    field.name_in_plan = form.cleaned_data['name_in_plan']
                    field.name_in_load = form.cleaned_data['name_in_load']
                    field.type_of_load = form.cleaned_data['type_of_load']
                    field.load_type = form.cleaned_data['load_type']
                    field.owner = request.user

                    fields_to_save.append(field)

            request.user.adopted_fields = request.user
            request.user.save()
            Field.objects.bulk_create(fields_to_save)

            fields = Field.objects.select_related('type_of_load').filter(owner=request.user.adopted_fields)
            formset = FieldFormSet(queryset=fields)

            context = {
                'forms': formset,
            }

    return render(request, template_name, context)


def search(request, template_name='builder/search.html'):
    if request.method == 'GET' and request.user.is_authenticated:
        text = request.GET['search'].split(' ')
        if request.GET['search'] == '':
            context = {
                'users': CustomUser.objects.all(),
            }

        queryset = set()
        for piece in text:
            for query in CustomUser.objects.filter(first_name__icontains=piece):
                queryset.add(query)
            for query in CustomUser.objects.filter(last_name__icontains=piece):
                queryset.add(query)
            for query in CustomUser.objects.filter(email__icontains=piece):
                queryset.add(query)

        context = {
            'users': queryset,
        }
        if request.user in queryset:
            queryset.remove(request.user)

        return render(request, template_name, context)


def default_fields(request):
    if request.user.is_authenticated:
        if request.user.adopted_fields is not None:
            Field.objects.filter(owner=request.user.adopted_fields).delete()
            request.user.adopted_fields = None
            request.user.save()
            for user in CustomUser.objects.filter(adopted_fields=request.user):
                user.adopted_fields = None
                user.save()

    return redirect('builder:edit_fields')


# def change_fields(request):
#     if request.method == 'GET' and request.user.is_authenticated:
#         if request.GET['adopt'] == '':
#             default_fields(request)
#         else:
#             request.user.adopted_fields = CustomUser.objects.get(pk=request.GET['adopt'])
#             request.user.save()
#
#     return redirect('builder:edit_fields')


def request_adopt(request):
    if request.method == 'GET' and request.user.is_authenticated:
        if request.GET['adopt'] == '':
            default_fields(request)
        else:
            new_request = Request()
            new_request.sender = request.user
            new_request.receiver = CustomUser.objects.get(pk=int(request.GET['adopt']))
            new_request.create_date = timezone.now()
            new_request.type = RequestType.objects.get(name='Adopt')
            new_request.save()
            print(new_request.id)
    return HttpResponse('empty')


def answer_request_adopt(request):
    if request.method == 'GET' and request.user.is_authenticated:
        new_request = Request.objects.get(pk=int(request.GET['request_id']))

        # danger
        if int(request.GET['answer']) == 0:
            new_request.result = RequestResultType.objects.get(name='False')
            new_request.answer_date = timezone.now()
            new_request.save()

        # success
        elif int(request.GET['answer']) == 1:
            new_request.result = RequestResultType.objects.get(name='True')
            new_request.sender.adopted_fields = new_request.receiver
            new_request.sender.save()
            new_request.answer_date = timezone.now()
            new_request.save()

        # cancel
        elif int(request.GET['answer']) == 2:
            new_request.delete()

    return HttpResponse('empty')


def requests(request, template_name='builder/requests.html'):
    if request.method == 'GET' and request.user.is_authenticated:
        request_out = Request.objects.filter(sender=request.user).order_by('answer_date')
        request_in = Request.objects.filter(receiver=request.user).order_by('answer_date')

        context = {
            'request_out': request_out,
            'request_in': request_in
        }

        return render(request, template_name, context)
