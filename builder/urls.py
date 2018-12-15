from django.urls import path
from .views import index, upload_load, get_subjects, build_plan, edit_fields, search, default_fields, request_adopt, answer_request_adopt, requests

urlpatterns = [
    path('', index, name='index'),
    path('file_upload', upload_load, name='file_upload'),
    path('load_subj', get_subjects, name='load_subj'),
    path('build_plan', build_plan, name='build_plan'),
    path('edit_fields', edit_fields, name='edit_fields'),
    path('search', search, name='search'),
    path('default_fields', default_fields, name='default_fields'),
    path('requests', requests, name='requests'),
    path('request_adopt', request_adopt, name='request_adopt'),
    path('answer_request_adopt', answer_request_adopt, name='answer_request_adopt'),
]
