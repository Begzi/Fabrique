
from django_seed import Seed
import json
from django.shortcuts import render, redirect, HttpResponse
from .models import Message


def index(request):
    my_messages = Message.objects.all()
    return render(request, 'messages/index.html', {'my_messages' : my_messages})

def create(request):
    pass
def storage(request):
    pass

def edit(request):
    pass

def delete(request):
    pass