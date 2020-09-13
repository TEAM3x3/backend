from action_serializer import ModelActionSerializer
from rest_framework.serializers import ModelSerializer

from .models import Event, MainEvent, MainEventType, GoodsEventType
from goods.serializers import GoodsSerializers, GoodsSaleSerializers


class EventSerializers(ModelActionSerializer):
    goods = GoodsSaleSerializers(many=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'image', 'goods')
        action_fields = {
            'list': {'fields': ('id', 'title', 'image')},
            'retrieve': {'fields': ('id', 'title', 'goods')},
        }


class GoodsEventTypeSerializers(ModelSerializer):
    goods = GoodsSaleSerializers()

    class Meta:
        model = GoodsEventType
        fields = ('goods',)


class MainEventTypeSerializers(ModelSerializer):
    mainEvent = GoodsEventTypeSerializers(many=True)

    class Meta:
        model = MainEventType
        fields = ('id', 'name', 'mainEvent')


class MainEventSerializers(ModelActionSerializer):
    event = MainEventTypeSerializers(many=True)

    class Meta:
        model = MainEvent
        fields = ('id', 'image', 'event')
        action_fields = {
            'list': {'fields': ('id', 'image',)},
            'retrieve': {'fields': ('id', 'event',)}
        }
