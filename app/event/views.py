from django.shortcuts import render

# Create your views here.
from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from event.serializers import EventSerializers, MainEventSerializers
from .models import Event, MainEvent


class EventAPIView(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializers


class MainEventAPIView(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = MainEvent.objects.all()
    serializer_class = MainEventSerializers
