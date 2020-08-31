from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from carts.models import CartItem, Cart


class CartItemSerializer(ModelSerializer):
    sub_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('id',
                  'cart',
                  'goods', 'quantity', 'sub_total')


    def get_sub_total(self, obj):
        return obj.sub_total()


class CartSerializer(ModelSerializer):
    item = CartItemSerializer(many=True)
    total_pay = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'item', 'total_pay')

    def get_total_pay(self, obj):
        return obj.total_pay
