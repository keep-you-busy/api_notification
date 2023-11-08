from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from api.serializer import ClientSerializer, NewsLetterSerializer, MessageSerializer
from users.models import Client, NewsLetter, Message


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']


class NewsLetterViewSet(ModelViewSet):
    queryset = NewsLetter.objects.all()
    serializer_class = NewsLetterSerializer


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
