import json
from django.shortcuts import render, redirect, HttpResponse
from .models import Filter, Notice, Notice_Filter
from .forms import NoticeValid
from django.core.paginator import Paginator
import datetime
from django.contrib import messages


def index(request):

    notices = Notice.objects.select_related().all()
    print(notices)
    print(notices[0].filter_table.all()[0].filter.id)
    return render(request, 'notices/index.html', {'notices' : notices})

def create(request):
    context={}
    filters = Filter.objects.all()
    context['filters'] = filters
    return render(request, 'notices/create.html', context)

def storage(request):
    notice_valid = NoticeValid(request.POST['ended'],request.POST['text'], request.POST.getlist('filters'))
    context = notice_valid.is_valid()
    if context['error'] == False:
        notice = Notice()
        notice.ended = request.POST['ended']
        notice.text = request.POST['text']
        notice.save()

        for filter in request.POST.getlist('filters'):
            notice_filter = Notice_Filter()
            notice_filter.filter_id = filter
            notice_filter.notice_id = notice.id
            notice_filter.save()


        return redirect('notice:index')

    for message in context['messages']:
        messages.add_message(request, messages.INFO, message)
    return redirect('notice:create')

def edit(request, notice_id):
    context={}
    notice = Notice.objects.get(id = notice_id)
    filters = Filter.objects.all()
    context['filters'] = filters
    notice.ended = str((notice.ended).date())
    context['notice'] = notice
    return render(request, 'notices/edit.html', context)

def update(request, notice_id):
    notice_valid = NoticeValid(request.POST['ended'],request.POST['text'], request.POST.getlist('filters'))
    context = notice_valid.is_valid()
    if context['error'] == False:
        notice = Notice.objects.get(id = notice_id)
        notice.ended = request.POST['ended']
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
