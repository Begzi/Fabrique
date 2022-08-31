from datetime import date

from rest_framework import serializers
from notice.forms import *

from .models import Filter, Notice, Notice_Filter
from client.models import Client


class FilterSerializer(serializers.Serializer):
    code = serializers.CharField()
    tag = serializers.CharField()

class Notice_FilterWriteSerializer(serializers.Serializer):
    filter = FilterSerializer()
    # filter = serializers.SlugRelatedField(slug_field='id', queryset=Filter.objects)

class MessageSerializer(serializers.Serializer):
    created = serializers.DateField(
        format='%d.%m.%Y',
        input_formats=['%d.%m.%Y', 'iso-8601'],
    )
    status = serializers.CharField( max_length= 25)
    client = serializers.SlugRelatedField(slug_field='phone', queryset=Client.objects)


class NoticeWriteSerializer(serializers.Serializer):
    text = serializers.CharField()
    ended = serializers.DateField(
        format='%d.%m.%Y',
        input_formats=['%d.%m.%Y', 'iso-8601'],
    )
    started = serializers.DateField(
        format='%d.%m.%Y',
        input_formats=['%d.%m.%Y', 'iso-8601'],
    )
    filters = Notice_FilterWriteSerializer(source='filter_table', many=True)
    message = MessageSerializer(source='messages',  many=True)

    def create(self,started, ended, text, filters):
        notice = Notice()
        notice.text = text
        notice.created = date.today().strftime('%Y-%m-%d')
        notice.started = started
        notice.ended = ended
        notice.save()

        for filter in filters:
            notice_filter = Notice_Filter()
            notice_filter.filter_id = filter
            notice_filter.notice_id = notice.id
            notice_filter.save()

        return {'messages': ['Успешное добавление']}

class NoticeEditSerializer(serializers.Serializer):
    text = serializers.CharField()
    ended = serializers.DateField(
        format='%d.%m.%Y',
        input_formats=['%d.%m.%Y', 'iso-8601'],
    )
    started = serializers.DateField(
        format='%d.%m.%Y',
        input_formats=['%d.%m.%Y', 'iso-8601'],
    )
    filters = serializers.ListField(child=serializers.IntegerField())


    def validate(self, attrs):
        return attrs

    def update(self, instance, validated_data):
        context = is_valid(str(validated_data['started']), str(validated_data['ended']), validated_data['text'], validated_data['filters'])

        if context['error']  == False:
            instance.text = validated_data['text']
            instance.ended = validated_data['ended']
            instance.started = validated_data['started']
            instance.save()
            filters_table = instance.filter_table.all()
            filters_past = []
            for filter_table in filters_table:
                filters_past.append(filter_table.filter.id)

            for filter in validated_data['filters']:
                if int(filter) in filters_past:
                    filters_past.remove(int(filter))
                else:
                    notice_filter = Notice_Filter()
                    notice_filter.filter_id = int(filter)
                    notice_filter.notice_id = instance.id
                    notice_filter.save()

            if len(filters_past) != 0:
                for bad_filter in filters_past:
                    Notice_Filter.objects.filter(filter_id = bad_filter).delete()

            return {'messages': ['Успешное изменено']}
        else:
            return context

class NoticeViewSerializer(serializers.Serializer):
    text = serializers.CharField()
    ended = serializers.DateField(
        format='%d.%m.%Y',
        input_formats=['%d.%m.%Y', 'iso-8601'],
    )
    started = serializers.DateField(
        format='%d.%m.%Y',
        input_formats=['%d.%m.%Y', 'iso-8601'],
    )
    filters = Notice_FilterWriteSerializer(source='filter_table', many=True)
    message = MessageSerializer(source='messages', many=True)
