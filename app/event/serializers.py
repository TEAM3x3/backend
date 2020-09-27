from action_serializer import ModelActionSerializer
from rest_framework.serializers import ModelSerializer

from .models import Event, MainEvent, MainEventType, GoodsEventType
from goods.serializers import GoodsSaleSerializers


class EventSerializers(ModelActionSerializer):
    goods = GoodsSaleSerializers(many=True)
    """
    goods(역관계)에서 가져오는 값들을 ordering 할 수 있는 방법 >> django filters를 사용해서?
    """
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
        fields = ('id', 'title', 'image', 'event')
        action_fields = {
            'list': {'fields': ('id', 'title', 'image',)},
            'retrieve': {'fields': ('id', 'title', 'detail_image', 'event',)}
        }
