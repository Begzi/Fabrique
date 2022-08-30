
from django_seed import Seed
import json
from django.shortcuts import render, redirect, HttpResponse
from .models import Message
from main.views import *


@check_notice_for_send_message_decorator
def index(request):
    my_messages = Message.objects.all()
    return render(request, 'messages/index.html', {'my_messages' : my_messages})

@check_notice_for_send_message_decorator
def create(request):
    pass
def storage(request):
    pass

def edit(request):
    pass

def delete(request):
    pass