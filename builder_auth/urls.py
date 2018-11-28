from django.urls import path, reverse_lazy

from django.contrib.auth.views import logout_then_login, LoginView
from django.views.generic import CreateView

from builder_auth.forms import CustomUserCreationForm
from builder_auth.views import LoginView, CreationView

app_name = 'builder_auth'

urlpatterns = [
    path('login/', LoginView, name='login'),

    path('logout/', logout_then_login, name='logout'),

    path('register/', CreationView, name='register'),
]

