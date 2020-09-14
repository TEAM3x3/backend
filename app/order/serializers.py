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
    discount_payment = serializers.SerializerMethodField()
    discount_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id',
                  'user',
                  'address',
                  'item',
                  'status',
                  'payment',
                  'discount_payment',
                  'discount_price',
                  )

    def get_payment(self, obj):
        return obj.total_payment()

    def get_discount_payment(self, obj):
        return obj.discount_payment()

    def get_discount_price(self, obj):
        return int(obj.total_payment() - obj.discount_payment())


class OrderCreateSerializers(ModelSerializer):
    class Meta:
        model = Order
        fields = ('id',
                  'user',
                  'address',
                  'item',
                  )


class ReviewCreateSerializers(ModelSerializer):
    class Meta:
        model = OrderReview
        fields = ('id', 'title', 'content', 'goods')
