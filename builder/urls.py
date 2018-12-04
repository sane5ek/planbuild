from django.urls import path
from .views import index, upload, subj

urlpatterns = [
    path('', index, name='index'),
    path('file_upload', upload, name='file_upload'),
    path('load_subj', subj, name='load_subj'),
]