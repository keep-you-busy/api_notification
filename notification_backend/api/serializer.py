import pytz
from rest_framework import serializers

from users.models import Client, NewsLetter, Message
from api.utils import set_clients_values, update_or_create_newsletter
from api.tasks import send_message


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

    def validate(self, attrs):
        start_datetime = attrs.get('start_datetime')
        end_datetime = attrs.get('end_datetime')
        if start_datetime > end_datetime:
            raise serializers.ValidationError(
                {'errors': 'Время начала рассылки позже окончания.'}
            )
        return super().validate(attrs)

    def create(self, validated_data):
        newsletter = update_or_create_newsletter(validated_data)
        messages = Message.objects.filter(newsletter__id__in=newsletter)
        for message in messages:
            send_message(message)
        return newsletter

    def update(self, instance, validated_data):
        newsletter = update_or_create_newsletter(validated_data, instance)
        messages = Message.objects.filter(newsletter__id__in=newsletter)
        for message in messages:
            send_message(message)
        return newsletter

    def to_representation(self, instance):
        newsletter_serializer = NewsLetterSerializer(instance,
                                                     context=self.context)
        return newsletter_serializer.data
