from django.urls import path
from .views import *
#из этой же директории импортирую

app_name = 'message'

urlpatterns = [
    path('', index, name = 'index'),
    path('create', create, name = 'create'),
    path('storage', storage, name = 'storage'),
    path('edit', edit, name = 'edit'),
    path('delete', delete, name = 'delete'),
]
