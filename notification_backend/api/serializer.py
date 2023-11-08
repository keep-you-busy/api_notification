import pytz
from rest_framework import serializers

from users.models import Client, NewsLetter, Message


class ClientSerializer(serializers.ModelSerializer):
    time_zone = serializers.ChoiceField(choices=pytz.all_timezones)

    class Meta:
        model = Client
        fields = (
            'id',
            'phone_number',
            'network_code',
            'tag',
            'time_zone'
        )
        read_only_fields = ('network_code',)


class NewsLetterSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsLetter
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'
