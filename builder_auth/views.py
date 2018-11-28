from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from builder_auth.forms import CustomUserCreationForm
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.forms.utils import ErrorList

from django.contrib.auth import authenticate, login

def LoginView(request, template_name='builder_auth/login.html', message=''):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Неверный адрес электронной почты или пароль.')
                context = {'email': username}
                return render(request, template_name, context)
        else:
            print(message)
            return render(request, template_name)

@csrf_protect
def CreationView(request, template_name='builder_auth/register.html'):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        context = {}
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Регистрация прошла успешно.')
                context['form'] = form
            else:
                error_list = []
                for field in form:
                    for error in field.errors.as_data():
                        if error.code == 'password_too_short':
                            error.message = 'Пароль слишком короткий.'
                        if error.code == 'password_too_common':
                            error.message = 'Пароль слишком простой.'
                        if error.code == 'password_too_similar':
                            error.message = 'Ваш пароль не может быть похож на личную информацию.'
                        if error.code == 'password_entirely_numeric':
                            error.message = 'Ваш пароль содержит только цифры.'
                        if error.code == 'unique':
                            error.message = 'Пользователь с такой почтой уже зарегистрирован.'
                        error_list.append(error)

                context['errors'] = ErrorList(error_list)
                print(context['errors'])

                context['form'] = form
        else:
            context['form'] = CustomUserCreationForm()

        return render(request, template_name, context)
