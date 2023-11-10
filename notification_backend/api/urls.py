from django.urls import include, path
from rest_framework import routers

from api.views import ClientViewSet, NewsLetterViewSet


router_v1 = routers.DefaultRouter()

router_v1.register(r'clients', ClientViewSet, basename='clients')
router_v1.register(r'newsletters', NewsLetterViewSet, basename='newsletters')

urlpatterns = [
    path('', include(router_v1.urls))
]
