from django.urls import path
from django.contrib.auth.views import logout_then_login

from .views import LoginView, CreationView, ChangeView

app_name = 'builder_auth'

urlpatterns = [
    path('login/', LoginView, name='login'),
    path('logout/', logout_then_login, name='logout'),
    path('register/', CreationView, name='register'),
    path('edit/', ChangeView, name='edit'),
]

