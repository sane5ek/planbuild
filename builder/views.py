from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse

def index(request, template_name='builder/index.html'):
    if not request.user.is_authenticated:
        return redirect('builder_auth:login')
    else:
        return render(request, 'builder/index.html')