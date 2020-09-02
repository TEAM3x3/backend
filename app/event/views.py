from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet

from event.serializers import EventSerializers
from .models import Event


class EventAPIView(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializers
