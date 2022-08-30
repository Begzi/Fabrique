from django.shortcuts import render
from notice.models import Notice
from message.models import Message
from client.models import Client
# Create your views here.
from django.core.cache import cache
from datetime import date

def create_messages(notice):
    if (notice.started <= date.today()):
        filters_notice = notice.filter_table.all()
        filters = []
        for filter in filters_notice:
            code = filter.filter.code
            if code != '' and code != None:
                filters.append(code)
            else:
                filters.append(filter.filter.tag)
        clients=[]
        for filter in filters:
            clients_code = Client.objects.filter(code=filter).all()
            if len(clients_code) != 0:
                for client_code in clients_code:
                    if client_code not in clients:
                        clients.append(client_code)
            else:
                clients_tag = Client.objects.filter(tag=filter).all()
                if len(clients_tag) != None:
                    for client_tag in clients_tag:
                        if client_tag not in clients:
                            clients.append(client_tag)
        for client in clients:
            message = Message()
            message.client = client
            message.notice = notice
            message.status = 'sent'
            message.save()
    else:
        pass

def check_notice_for_send_message_decorator(function_to_decorate):

    def check_notice(request):
        if cache.get('my_key') == None:
            cache.set('my_key', 'check_notice', 60*60*24)
            notices = Notice.objects.filter(started__lte =  date.today()).all()
            for notice in notices:
                messages = notice.messages.all()
                if len(messages) == 0:
                    create_messages(notice)
        tmp = function_to_decorate(request)
        return tmp
    return check_notice


@check_notice_for_send_message_decorator
def main(request):

    return render(request, 'index.html')