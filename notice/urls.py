from django.urls import path
from .views import *
#из этой же директории импортирую

app_name = 'notice'

urlpatterns = [
    path('', index, name = 'index'),
    path('create', create, name = 'create'),
    path('storage', storage, name = 'storage'),
    path('edit<int:notice_id>', edit, name = 'edit'),
    path('update<int:notice_id>', update, name = 'update'),
    path('delete<int:notice_id>', delete, name = 'delete'),
]
