from rest_framework.serializers import ModelSerializer
from carts.models import CartItem


class CartItemSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('user', 'goods', 'quantity',)
