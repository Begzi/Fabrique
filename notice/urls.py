from django.urls import path
from .views import *
#из этой же директории импортирую
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

app_name = 'notice'
# schema_view = get_schema_view(
#    openapi.Info(
#       title="Snippets API",
#       default_version='v1',
#       description="Test description",
#       terms_of_service="https://probe.fbrq.cloud/v1",
#       contact=openapi.Contact(email="contact@snippets.local"),
#       license=openapi.License(name="BSD License"),
#    ),
#    public=True,
#    permission_classes=[permissions.AllowAny],
# )
urlpatterns = [
    path('', index, name = 'index'),
    path('create', create, name = 'create'),
    path('storage', storage, name = 'storage'),
    path('edit<int:notice_id>', edit, name = 'edit'),
    path('update<int:notice_id>', update, name = 'update'),
    path('delete<int:notice_id>', delete, name = 'delete'),
    path('api/show', GetNoticeInfoView.as_view()),
    path('api/create', GetNoticeWriteInfoView.as_view()),
    path('api/edit<int:id>', GetNoticeEditInfoView.as_view()),
    path('api/delete<int:id>', GetNoticeEditInfoView.as_view()),
    path('api/view<int:id>', GetNoticeViewInfoView.as_view()),
    # path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # path('api/delete<int:id>', GetNoticeUpdateView.as_view()),
]
