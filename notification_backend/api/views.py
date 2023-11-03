from rest_framework.viewsets import ModelViewSet

from api.serializer import ClientSerializer, NewsLetterSerializer, MessageSerializer
from users.models import Client, NewsLetter, Message


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class NewsLetterViewSet(ModelViewSet):
    queryset = NewsLetter.objects.all()
    serializer_class = NewsLetterSerializer


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
