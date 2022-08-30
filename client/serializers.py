from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from client.models import TimeZone, Client
from notice.models import Filter


class ClientSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=12)
    code = serializers.CharField(max_length=5)
    tag = serializers.CharField(max_length=15)
    time_zone = serializers.CharField(source='time_zone.title', max_length=30)

class ClientWriteSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=12)
    code = serializers.CharField(max_length=5)
    tag = serializers.CharField(max_length=15)
    time_zone = serializers.SlugRelatedField(slug_field='title', queryset=TimeZone.objects)

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=Client.objects,
                fields=['phone']
            )
        ]

    def validate(self, attrs):
        set_attrs = set(
            [attrs['phone'], attrs['code'], attrs['tag']]
        )
        if len(set_attrs) != 3:
            raise ValidationError(
                'Номер телефона, код и тег не могут совпадать между собой',
                code='duplicate values'
            )
        return attrs

    def create(self, validated_data):
        if validated_data['code'] != None or validated_data['code'] != '':
            if Filter.objects.filter(code=validated_data['code']):
                pass
            else:
                filter = Filter()
                filter.code = validated_data['code']
                filter.save()
        if validated_data['tag'] != None or validated_data['tag'] != '':
            if Filter.objects.filter(code=validated_data['tag']):
                pass
            else:
                filter = Filter()
                filter.tag = validated_data['tag']
                filter.save()
        return Client.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if instance.code != validated_data['code']:
            if validated_data['code'] != None or validated_data['code'] != '':
                if Filter.objects.filter(code = instance.code) and len(Client.objects.filter(code = instance.code).all()) == 1:
                    Filter.objects.filter(code = instance.code) .delete()
                if Filter.objects.filter(code=validated_data['code']):
                    pass
                else:
                    filter = Filter()
                    filter.code = validated_data['code']
                    filter.save()
        if instance.tag != validated_data['tag']:
            if validated_data['tag'] != None or validated_data['tag'] != '':
                if Filter.objects.filter(tag = instance.tag) and len(Client.objects.filter(tag = instance.tag).all()) == 1:
                    Filter.objects.filter(tag = instance.tag) .delete()
                if Filter.objects.filter(tag=validated_data['tag']):
                    pass
                else:
                    filter = Filter()
                    filter.tag = validated_data['tag']
                    filter.save()
        instance.phone = validated_data['phone']
        instance.code = validated_data['code']
        instance.tag = validated_data['tag']
        instance.time_zone = validated_data['time_zone']
        instance.save()

        return instance

