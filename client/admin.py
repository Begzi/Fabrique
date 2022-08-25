from django.contrib import admin

from .models import TimeZone, Client
# Register your models here.

admin.site.register(TimeZone)
admin.site.register(Client)