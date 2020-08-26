from rest_framework import serializers

from carts.models import CartItem
from goods.serializers import GoodsSerializers


class CartItemSerializer(serializers.ModelSerializer):
    goods = GoodsSerializers()
    price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('goods', 'quantity', 'price',)

    def get_price(self, obj):
        return (obj.goods.price * obj.quantity)
