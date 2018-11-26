from django.urls import path

from django.contrib.auth.views import logout_then_login, LoginView
from django.views.generic import CreateView

from builder_auth.forms import CustomUserCreationForm

app_name = 'builder_auth'

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='builder_auth/login.html'
    ), name='login'),

    path('logout/', logout_then_login, name='logout'),

    path('register/', CreateView.as_view(
        template_name='builder_auth/register.html',
        form_class=CustomUserCreationForm,
        success_url='/',
    ), name='register'),
]
