from rest_framework import mixins, filters
from rest_framework.viewsets import GenericViewSet

from event.serializers import EventSerializers, MainEventSerializers
from .models import Event, MainEvent


class EventAPIView(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializers
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['goods__price', 'goods__sales__discount_rate']


class MainEventAPIView(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = MainEvent.objects.all()
    serializer_class = MainEventSerializers
