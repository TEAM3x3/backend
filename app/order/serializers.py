from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from carts.serializers import CartItemSerializer
from members.serializers import UserSerializer, UserAddressSerializers
from order.models import Order


class OrderListSerializers(ModelSerializer):
    item = CartItemSerializer(many=True)
    user = UserSerializer()
    address = UserAddressSerializers()
    payment = serializers.SerializerMethodField()

    class Meta:
        model = Order
<<<<<<< HEAD
        fields = ('id', 'user', 'address', 'item', 'payment')
=======
        fields = ('id',
                  'user',
                  'address',
                  'item',
                  'payment'
                  )
>>>>>>> aac0997f205ffeac4d97c8d453b3b32fde671294

    def get_payment(self, obj):
        return obj.total_payment()


class OrderCreateSerializers(ModelSerializer):
    class Meta:
        model = Order
<<<<<<< HEAD
        fields = ('id', 'user', 'address', 'item')
=======
        fields = ('id',
                  'user',
                  'address',
                  'item',
                  )
>>>>>>> aac0997f205ffeac4d97c8d453b3b32fde671294

    def create(self, validated_data):
        return super().create(validated_data)
