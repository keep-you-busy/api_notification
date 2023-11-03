from rest_framework import serializers

from users.models import Client, NewsLetter, Message


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = '__all__'


class NewsLetterSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsLetter
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'