from rest_framework.viewsets import ModelViewSet
from api.serializer import ClientSerializer, NewsLetterSerializer, NewsLetterCreateSerializer, MessageSerializer
from users.models import Client, NewsLetter, Message
from rest_framework.permissions import SAFE_METHODS


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']


class NewsLetterViewSet(ModelViewSet):
    queryset = NewsLetter.objects.all()
    serializer_class = NewsLetterSerializer

    def get_serializer_class(self):
        method = self.request.method
        if method in SAFE_METHODS:
            self.serializer_class = NewsLetterSerializer
        elif method == 'POST':
            self.serializer_class = NewsLetterCreateSerializer
        elif method == 'PATCH':
            self.serializer_class = NewsLetterCreateSerializer
        return self.serializer_class


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
