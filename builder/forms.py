from django import forms

from builder.models import UploadFile


class UploadFileForm(forms.ModelForm):

    class Meta:
        model = UploadFile
        fields = ('file',)