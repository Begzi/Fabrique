import json
from django.shortcuts import render, redirect, HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from client.models import Client
from .models import Filter, Notice, Notice_Filter
from message.models import Message
from .forms import *
from django.core.paginator import Paginator
from datetime import date, datetime
from django.contrib import messages
from main.views import *
from .serializers import *
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer

@check_notice_for_send_message_decorator
def index(request):

    notices = Notice.objects.select_related().all()
    return render(request, 'notices/index.html', {'notices' : notices})

@check_notice_for_send_message_decorator
def create(request):
    context={}
    filters = Filter.objects.all()
    context['filters'] = filters
    return render(request, 'notices/create.html', context)

def storage(request):
    context = is_valid(request.POST['started'],request.POST['ended'], request.POST['text'], request.POST.getlist('filters'))
    if context['error'] == False:
        notice = Notice()
        notice.ended = datetime.strptime(request.POST['ended'], '%Y-%m-%d').date()
        notice.text = request.POST['text']
        notice.started = datetime.strptime(request.POST['started'], '%Y-%m-%d').date()
        notice.save()

        for filter in request.POST.getlist('filters'):
            notice_filter = Notice_Filter()
            notice_filter.filter_id = filter
            notice_filter.notice_id = notice.id
            notice_filter.save()

        create_messages(notice)
        return redirect('notice:index')

    for message in context['messages']:
        messages.add_message(request, messages.INFO, message)
    return redirect('notice:create')

def edit(request, notice_id):
    context={}
    notice = Notice.objects.get(id = notice_id)
    filters = Filter.objects.all()
    context['filters'] = filters
    notice.ended = str((notice.ended).strftime('%Y-%m-%d'))
    notice.started = str((notice.started).strftime('%Y-%m-%d'))
    context['notice'] = notice
    return render(request, 'notices/edit.html', context)

def update(request, notice_id):
    context = is_valid(request.POST['started'], request.POST['ended'], request.POST['text'],
                       request.POST.getlist('filters'))

    if context['error'] == False:
        notice = Notice.objects.get(id = notice_id)
        notice.ended = request.POST['ended']
        notice.started = request.POST['started']
        notice.text = request.POST['text']
        notice.save()

        filters_table = notice.filter_table.all()
        filters = []
        for filter_table in filters_table:
            filters.append(filter_table.filter.id)


        for filter in request.POST.getlist('filters'):
            if int(filter) in filters:
                filters.remove(int(filter))
            else:
                notice_filter = Notice_Filter()
                notice_filter.filter_id = int(filter)
                notice_filter.notice_id = notice.id
                notice_filter.save()

        if len(filters) != 0:
            for bad_filter in filters:
                Notice_Filter.objects.filter(filter_id = bad_filter).delete()


        return redirect('notice:index')

    for message in context['messages']:
        messages.add_message(request, messages.INFO, message)
    return redirect('notice:edit' + notice_id)

def delete(request, notice_id):
    Notice.objects.filter(id = notice_id).delete()
    return redirect('notice:index')



class GetNoticeInfoView(APIView):
    serializer_class = NoticeWriteSerializer
    model = Notice

    def get(self, request):
        queryset = self.model.objects.all()
        serializer_for_queryset = self.serializer_class(
            instance=queryset,
            many=True
        )
        return Response(serializer_for_queryset.data)

class GetNoticeWriteInfoView(APIView):
    serializer_class = NoticeWriteSerializer
    model = Notice

    def get(self, request):
        context={}
        filters = Filter.objects.all()
        context['filters'] = filters
        return Response(context)

    def post(self, request):
        context = is_valid(request.POST['started'], request.POST['ended'], request.POST['text'],
                           request.POST.getlist('filters'))

        if context['error']:
            return Response(context)
        else:
            serializer_for_writing = self.serializer_class(data=request.data)
            serializer_for_writing.create(request.POST['started'],request.POST['ended'],request.POST['text'], request.POST.getlist('filters'))
        return Response(context)


class GetNoticeEditInfoView(APIView):
    serializer_class = NoticeEditSerializer
    model = Notice

    def get(self, request, id):
        queryset = self.model.objects.all()
        serializer_for_queryset = self.serializer_class(
            instance=queryset,
            many=True
        )
        return Response(serializer_for_queryset.data)

    def put(self, request, id):
        try:
            instance = Notice.objects.get(id=id)
        except:
            return Response({"error": "Такого Notice не существует"})

        serializer_for_updating = self.serializer_class(data=request.data, instance=instance)
        serializer_for_updating.is_valid(raise_exception=True)
        serializer_for_updating.save()
        return Response(
            data=serializer_for_updating.data,
            status=status.HTTP_202_ACCEPTED
        )

    def delete(self, request, id):

        try:
            instance = Notice.objects.get(id=id)
        except:
            return Response({"error": "Такого Notice не существует"})

        instance.delete()

        return Response({'messages': ['Успешное удаление']})



class GetNoticeViewInfoView(APIView):
    serializer_class = NoticeViewSerializer
    model = Notice
    def get(self, request, id):
        queryset = self.model.objects.filter(id=id).all()
        serializer_for_queryset = self.serializer_class(
            instance=queryset,
            many=True
        )
        return Response(serializer_for_queryset.data)