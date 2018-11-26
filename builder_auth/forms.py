# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from builder_auth.models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'post', 'salary', 'science_degree', 'science_title')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

