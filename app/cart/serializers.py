from rest_framework.serializers import ModelSerializer

from cart.models import Cart, CartItem


class CartSerializers(ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id', 'cart_id', 'date_added')


class CartItemSerializers(ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'goods', 'quantity', 'created_at')
