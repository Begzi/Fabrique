from django.urls import path
from .views import *
#из этой же директории импортирую

app_name = 'client'

urlpatterns = [
    path('', index, name = 'index'),
    path('create', create, name = 'create'),
    path('storage', storage, name = 'storage'),
    path('edit<int:client_id>', edit, name = 'edit'),
    path('update<int:client_id>', update, name = 'update'),
    path('delete<int:client_id>', delete, name = 'delete'),
    path('seed', seed, name = 'seed'),
]
