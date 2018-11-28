# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from builder_auth.models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    error_messages = {
        'password_mismatch': _("Пароли не совпадают."),
        'password_too_short': _('Слишком короткий'),
    }

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'post', 'salary', 'science_degree', 'science_title')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['post'].required = True
        self.fields['salary'].required = True
        self.fields['science_degree'].required = False

        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['email'].label = 'Адрес электронной почты'
        self.fields['post'].label = 'Должность'
        self.fields['salary'].label = 'Ставка'
        self.fields['science_degree'].label = 'Научная степень'
        self.fields['science_title'].label = 'Научное звание'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'



        self.fields['password1'].help_text = mark_safe('<ul><li>Ваш пароль не может быть похож на другую личную информацию.</li><li>Ваш пароль должен содержать хотя бы 8 символов.</li><li>Ваш пароль должен быть сложным.</li><li>Ваш пароль не может состоять только из цифр.</li></ul>')
        self.fields['password2'].help_text = mark_safe('Введите точно такой же пароль для подтверждения.')

        self.fields['post'].empty_label = 'Выберите должность'
        self.fields['science_degree'].empty_label = 'Выберите научную степень'
        self.fields['science_title'].empty_label = 'Выберите научное звание'
        for visible in self.visible_fields():

            visible.field.widget.attrs['class'] = 'form-control mb-3 mt-1 bg-dark text-white'
            visible.field.widget.attrs['placeholder'] = visible.label
            if visible.errors:
                visible.field.widget.attrs['class'] += ' is-invalid'

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username',)

class CustomAuthenticationForm(AuthenticationForm):

    class Meta:
        model=CustomUser
        fields = ('username',)
