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
        fields = ('goods', 'user', 'quantity')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=CartItem.objects.all(),
                fields=('goods', 'user'),
                message=("이미 장바구니에 있는 상품입니다.")
            )
        ]

class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('quantity',)