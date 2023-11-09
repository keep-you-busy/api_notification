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
            'network_codes',
            'text',
        )

    def get_tags(self, newsletter):
        return set_clients_values(newsletter, 'tag')

    def get_network_codes(self, newsletter):
        return set_clients_values(newsletter, 'network_code')


class NewsLetterCreateSerializer(serializers.ModelSerializer):
    start_datetime = serializers.DateTimeField(
        required=True,
        )
    end_datetime = serializers.DateTimeField(
        required=True,
        )
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),
        )
    network_codes = serializers.ListField(
        child=serializers.CharField(max_length=3),
        )

    class Meta:
        model = NewsLetter
        fields = (
            'start_datetime',
            'end_datetime',
            'tags',
            'network_codes',
            'text',
        )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        network_codes = validated_data.pop('network_codes')
        clients = Client.objects.filter(
            tag__in=tags,
            network_code__in=network_codes)
        newsletter = NewsLetter.objects.create(**validated_data)
        newsletter.clients.set(clients)
        return newsletter

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        network_codes = validated_data.pop('network_codes')
        instance.start_datetime = validated_data.get(
            'start_datetime', instance.start_datetime
        )
        instance.end_datetime = validated_data.get(
            'end_datetime', instance.end_datetime
        )
        instance.text = validated_data.get(
            'text', instance.text
        )
        instance.clients.clear()
        clients = Client.objects.filter(
            tag__in=tags,
            network_code__in=network_codes)
        for client in clients:
            Message.objects.update_or_create(
                newsletter=instance,
                client=client
            )
        instance.save()

        return instance

    def to_representation(self, instance):
        newsletter_serializer = NewsLetterSerializer(instance,
                                                     context=self.context)
        return newsletter_serializer.data


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'
