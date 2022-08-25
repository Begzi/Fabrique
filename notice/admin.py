from django.contrib import admin

from .models import Filter, Notice, Notice_Filter

# Register your models here.

admin.site.register(Filter)
admin.site.register(Notice)
admin.site.register(Notice_Filter)
