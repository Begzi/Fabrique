
from django_seed import Seed
import json
from django.shortcuts import render, redirect, HttpResponse
from rest_framework import status

from .models import TimeZone, Client
from .forms import ClientValid
from notice.models import Filter
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ClientSerializer, ClientWriteSerializer
from main.views import *

@check_notice_for_send_message_decorator
def index(request):
    clients = Client.objects.all()
    return render(request, 'clients/index.html', {'clients' : clients})

@check_notice_for_send_message_decorator
def create(request):
    context={}
    timezone = TimeZone.objects.all()
    context['timezone'] = timezone
    return render(request, 'clients/create.html', context)

def help_storage(code, tag):
    if code != None or code != '':
        if Filter.objects.filter(code=code):
            pass
        else:
            filter = Filter()
            filter.code = code
            filter.save()
    if tag != None or tag != '':
        if Filter.objects.filter(code=tag):
            pass
        else:
            filter = Filter()
            filter.tag = tag
            filter.save()

def storage(request):
    client_valid = ClientValid(request.POST['phone'],request.POST['code'], request.POST['tag'], request.POST['time_zone_id'])
    context = client_valid.is_valid()
    if context['error'] == False:
        client = Client()
        client.phone = request.POST['phone']
        client.code = request.POST['code']
        client.tag = request.POST['tag']
        client.time_zone_id = request.POST['time_zone_id']
        client.save()

        help_storage(client.code, client.tag)

        return redirect('client:index')
    for message in context['messages']:
        messages.add_message(request, messages.INFO, message)
    return redirect('client:create')

def edit(request, client_id):
    context={}
    timezone = TimeZone.objects.all()
    client = Client.objects.get(id = client_id)
    context['timezone'] = timezone
    context['client'] = client
    return render(request, 'clients/edit.html', context)

def update(request, client_id):
    client_valid = ClientValid(request.POST['phone'], request.POST['code'], request.POST['tag'],
                               request.POST['time_zone_id'])
    context = client_valid.is_valid()
    if context['error'] == False:
        client = Client.objects.get(id = client_id)

        if (client.code != request.POST['code']):
            if Filter.objects.filter(code = client.code) and len(Client.objects.filter(code = client.code).all()) == 1:
                Filter.objects.filter(code=client.code).delete()
        if (client.tag != request.POST['tag']):
            if Filter.objects.filter(tag = client.tag) and len(Client.objects.filter(tag = client.tag).all()) == 1:
                Filter.objects.filter(tag=client.tag).delete()

        client.phone = request.POST['phone']
        client.code = request.POST['code']
        client.tag = request.POST['tag']
        client.time_zone_id = request.POST['time_zone_id']
        client.save()

        help_storage(client.code, client.tag)

        return redirect('client:index')
    for message in context['messages']:
        messages.add_message(request, messages.INFO, message)
    return redirect('client:edit' + str(client_id))

def delete(request, client_id):
    client = Client.objects.get(id = client_id)
    if Filter.objects.filter(code = client.code) and len(Client.objects.filter(code = client.code).all()) == 1:
        Filter.objects.filter(code=client.code).delete()
    if Filter.objects.filter(tag = client.tag) and len(Client.objects.filter(tag = client.tag).all()) == 1:
        Filter.objects.filter(tag=client.tag).delete()
    client.delete()
    return redirect('client:index')

def seed(request):
    seeder = Seed.seeder()
    seeder.add_entity(Client, 10)

    seeder.execute()

    clients = Client.objects.all()
    for client in clients:
        help_storage(client.code, client.tag)
    return HttpResponse(123)


class GetClientInfoView(APIView):

    def get(self, request):
        # Извлекаем набор всех записей из таблицы Capital
        queryset = Client.objects.all()
        # Создаём сериалайзер для извлечённого наборa записей
        serializer_for_queryset = ClientSerializer(
            instance=queryset,  # Передаём набор записей
            many=True  # На вход подается именно набор, а не одна запись
        )
        return Response(serializer_for_queryset.data)

class GetClientWriteView(APIView):
    serializer_class = ClientWriteSerializer
    model = Client

    def get(self, request):
        # Извлекаем набор всех записей из таблицы Writer
        # Создаём сериалайзер для извлечённого наборa записей
        serializer_for_reading = self.serializer_class(
            instance=self.model.objects.all(),  # Передаём набор записей
            many=True  # На вход подается именно набор, а не одна запись
        )
        return Response(serializer_for_reading.data)

    def post(self, request):
        serializer_for_writing = self.serializer_class(data=request.data)
        serializer_for_writing.is_valid(raise_exception=True)
        serializer_for_writing.save()
        return Response(
            data=serializer_for_writing.data,
            status=status.HTTP_201_CREATED
        )

class GetClientEditView(APIView):
    serializer_class = ClientWriteSerializer
    model = Client

    def get(self, request, id):
        # Извлекаем набор всех записей из таблицы Writer
        # Создаём сериалайзер для извлечённого наборa записей
        serializer_for_reading = self.serializer_class(
            instance=self.model.objects.filter(id=id),  # Передаём набор записей
            many=True  # На вход подается именно набор, а не одна запись
        )
        return Response(serializer_for_reading.data)
    def put(self, request, id):

        try:
            instance = Client.objects.get(id=id)
        except:
            return Response({"error": "Такого Client не существует"})

        serializer_for_updating = self.serializer_class(data=request.data, instance=instance)
        serializer_for_updating.is_valid(raise_exception=True)
        serializer_for_updating.save()
        return Response(
            data=serializer_for_updating.data,
            status=status.HTTP_202_ACCEPTED
        )

    def delete(self, request, id):

        try:
            instance = Client.objects.get(id=id)
        except:
            return Response({"error": "Такого Client не существует"})


        if Filter.objects.filter(code = instance.code) and len(Client.objects.filter(code = instance.code).all()) == 1:
            Filter.objects.filter(code=instance.code).delete()
        if Filter.objects.filter(tag = instance.tag) and len(Client.objects.filter(tag = instance.tag).all()) == 1:
            Filter.objects.filter(tag=instance.tag).delete()
        instance.delete()

        return Response(
            status=status.HTTP_200_OK
        )
