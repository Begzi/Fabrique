
from django_seed import Seed
import json
from django.shortcuts import render, redirect, HttpResponse
from .models import TimeZone, Client
from .forms import ClientValid
from notice.models import Filter
from django.contrib import messages



def index(request):
    clients = Client.objects.all()
    return render(request, 'clients/index.html', {'clients' : clients})

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
                if Filter.objects.filter(code=code):
                    pass
                else:
                    filter = Filter()
                    filter.tag = tag
                    filter.save()
    elif tag != None or tag != '':
        if Filter.objects.filter(code=code):
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
    seeder.add_entity(TimeZone, 5)
    seeder.add_entity(Client, 10)

    seeder.execute()

    clients = Client.objects.all()
    for client in clients:
        if client.code != None or client.code != '':
            filter = Filter()
            filter.code = client.code
            filter.save()
            if client.tag != None or client.tag != '':
                filter = Filter()
                filter.tag = client.tag
                filter.save()
        elif client.tag != None or client.tag != '':
            filter = Filter()
            filter.tag = client.tag
            filter.save()
    return HttpResponse(123)