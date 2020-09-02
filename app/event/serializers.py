from rest_framework.serializers import ModelSerializer

from .models import Event
from goods.serializers import GoodsSerializers


class EventSerializers(ModelSerializer):
    goods = GoodsSerializers(many=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'image', 'goods')
