import os

def get_absolute_path(path):
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\' + path.replace('/', '\\')