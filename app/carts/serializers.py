from rest_framework import serializers
from carts.models import CartItem
from goods.serializers import MinimumGoodsSerializers


class CartItemListSerializer(serializers.ModelSerializer):
    goods = MinimumGoodsSerializers(read_only=True)
    price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('id', 'goods', 'quantity', 'price',)


    def get_price(self, obj):
        return (obj.goods.price * obj.quantity)




class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('goods', 'quantity', 'user')


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('quantity',)