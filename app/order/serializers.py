from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from carts.serializers import CartItemSerializer
from members.serializers import UserSerializer, UserAddressSerializers
from order.models import Order, OrderReview


class OrderListSerializers(ModelSerializer):
    item = CartItemSerializer(many=True)
    user = UserSerializer()
    address = UserAddressSerializers()
    payment = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id',
                  'user',
                  'address',
                  'item',
                  'payment'
                  )

    def get_payment(self, obj):
        return obj.total_payment()


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


class ReviewCreateSerializers(ModelSerializer):
    class Meta:
        model = OrderReview
        fields = ('id', 'title', 'content', 'goods')
