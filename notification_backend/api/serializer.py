import pytz
from rest_framework import serializers

from users.models import Client, NewsLetter, Message
from api.utils import set_clients_values

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
    tags = serializers.SerializerMethodField()
    network_codes = serializers.SerializerMethodField()

    class Meta:
        model = NewsLetter
        fields = (
            'id',
            'start_datetime',
            'end_datetime',
            'tags',
            'network_codes'
        )

    def get_tags(self, newsletter):
        return set_clients_values(newsletter, 'tag')

    def get_network_codes(self, newsletter):
        return set_clients_values(newsletter, 'network_code')


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'
