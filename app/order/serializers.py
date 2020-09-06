from rest_framework.serializers import ModelSerializer

from carts.serializers import CartItemSerializer
from members.serializers import UserSerializer, UserAddressSerializers
from order.models import Order


class OrderListSerializers(ModelSerializer):
    item = CartItemSerializer(many=True)
    user = UserSerializer()
    address = UserAddressSerializers()

    class Meta:
        model = Order
        fields = ('id',
                  'user',
                  'address',
                  'item',
                  )


class OrderCreateSerializers(ModelSerializer):
    class Meta:
        model = Order
        fields = ('id',
                  'user',
                  'address',
                  'item',
                  )

    def create(self, validated_data):
        return super().create(validated_data)
