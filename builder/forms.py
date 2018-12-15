from django import forms
from django.forms import Select, TextInput

from .models import UploadFile, Field, Load


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = ('file',)


class FieldChangeForm(forms.ModelForm):
    type_of_load = forms.ModelChoiceField(queryset=Load.objects.all(), widget=forms.TextInput, disabled=True)
    column_in_plan = forms.TextInput()
    class Meta:
        model = Field
        fields = (
                     'column_in_load', 'column_in_plan', 'name_in_load', 'name_in_plan', 'load_type', 'type_of_load',
                     'owner')
        extra = 0
        exclude = ('owner',)
        max_num = 1
        widgets = {'type_of_load': TextInput(),
                   'id': TextInput(attrs={'required': False}),
                   'column_in_plan': TextInput(attrs={'disabled': True, 'required': False}),
                   'name_in_plan': TextInput(attrs={'disabled': True, 'required': False})}
