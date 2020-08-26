from rest_framework.serializers import ModelSerializer
from carts.models import CartItem, Cart


class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = ('cart_id', 'created_at',)


class CartSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('user', 'goods', 'quantity',)