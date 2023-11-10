from rest_framework.viewsets import ModelViewSet
from api.serializer import ClientSerializer, NewsLetterSerializer, NewsLetterCreateSerializer
from users.models import Client, NewsLetter, Message
from rest_framework.permissions import SAFE_METHODS
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from api.utils import retrieve_messages_statistic


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')


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

    @action(methods=('GET',),
            detail=False,
            url_path='statistic',
            url_name='statistic')
    def get_statistic(self, request):
        response = retrieve_messages_statistic(
            Message.objects)
        response['total_newsletters'] = NewsLetter.objects.count()

        return Response(response, status=status.HTTP_200_OK)

    @action(methods=('GET',),
            detail=True,
            url_path='statistic',
            url_name='statistic')
    def get_detailed_statistic(self, request, pk):
        response = retrieve_messages_statistic(
            Message.objects.filter(newsletter=pk))

        return Response(response, status=status.HTTP_200_OK)
